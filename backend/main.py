import os
import time
from http.client import HTTPException

from datetime import datetime
from fastapi import FastAPI, HTTPException, Body, responses, status
from fastapi.middleware.cors import CORSMiddleware
from robonomicsinterface import Account, Datalog
import cv2
import threading
import json

import mongodb_util
import ipfs_utils
import graph_constructor
import passport_generator
import qr_printer

with open('config.json') as config_file:
    config = json.load(config_file)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables to manage the capture state
is_recording = False
capture_thread = None
rtsp_url = config['rtsp_url']  # Replace with your RTSP stream URL


def capture_rtsp_stream():
    global is_recording

    # Create VideoCapture object to read from the RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'vp80')
    output_file = config["video_name"]
    fps = 30  # Output frames per second for the video
    out = cv2.VideoWriter(output_file, fourcc, fps, (config['width'], config['height']))  # Adjust resolution as needed

    frame_counter = 0
    timelapse_factor = config['timelapse_factor']  # Capture every 200th frame

    while is_recording:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_counter % timelapse_factor == 0:
            out.write(frame)

        frame_counter += 1

    cap.release()
    out.release()

@app.post("/start")
async def start_recording(name: str):
    print(1)
    global is_recording, capture_thread

    if type(name) != str or name == "":
        raise HTTPException(status_code=400, detail="Query parameter 'name' is required.")
    if is_recording:
        raise HTTPException(status_code=400, detail="Recording is ongoing.")

    mongo = mongodb_util.MongoDBUtil(config['mongo_connection_uri'], config['database_name'], "esp_data")
    mongo.remove_all_items()
    print("Mongo esp_data collection cleaned")

    if not is_recording:
        is_recording = True
        capture_thread = threading.Thread(target=capture_rtsp_stream)
        capture_thread.start()
        print("Recording has started")
    else:
        raise HTTPException(status_code=400, detail="Recording is already in progress.")

    mongo = mongodb_util.MongoDBUtil(config['mongo_connection_uri'], config['database_name'], "pictures")
    mongo.add_item({
        "name": name,
        "video_cid": None,
        "graph_cid": None,
        "passport_cid": None,
        "passport_link": None,
        "transaction": None,
        "esp_addr": None,
        "date": datetime.now()
    })
    print("Mongo pictures collection entry created")

    return {"message": "Recording started."}

@app.post("/stop")
async def stop_recording():
    global is_recording

    if is_recording:
        is_recording = False
        capture_thread.join()  # Wait for the thread to finish
        print("Recording stopped.")

        time.sleep(1)
        print("Uploading video.")
        video_cid, video_size = ipfs_utils.upload_file(os.path.abspath(config["video_name"]))
        print(video_cid, video_size)
        os.remove(config["video_name"])

        print("Generating graph.")
        mongo = mongodb_util.MongoDBUtil(config['mongo_connection_uri'], config['database_name'], "esp_data")
        esp_data = mongo.get_esp_data()
        esp_addr = esp_data[0]
        timestamps = esp_data[1]["Timestamps"]
        humidities = esp_data[1]["Humidities"]
        temperatures = esp_data[1]["Temperatures"]
        graph_constructor.generate_graph(timestamps=timestamps, humidities=humidities, temperatures=temperatures)

        print("Uploading graph.")
        graph_cid, graph_size = ipfs_utils.upload_file(os.path.abspath(config["graph"]))
        print(graph_cid, graph_size)
        os.remove(config["graph"])

        print("Updating mongo entry")
        mongo = mongodb_util.MongoDBUtil(config['mongo_connection_uri'], config['database_name'], "pictures")
        item = mongo.get_latest_item()
        mongo.modify_item(item, {"video_cid": video_cid, "graph_cid": graph_cid, "esp_addr": esp_addr})

        print("Generating passport")
        passport_path = passport_generator.generate_passport(item["name"], item["esp_addr"], video_cid, graph_cid)

        print("Uploading passport")
        passport_cid, passport_size = ipfs_utils.upload_file(passport_path)
        passport_link = f"{config['ipfs_prefix']}{passport_cid}"
        print(passport_cid, passport_size)

        print("Adding passport_cid to mongoDB")
        mongo.modify_item(item, {"passport_cid": passport_cid, "passport_link": passport_link})

        print("Sending passport to Robonomics Parachain")
        robonomics = Account(seed=config["seed"], remote_ws=config["remote_ws"])
        datalog = Datalog(robonomics)
        transaction = f"{config['explorer_prefix']}{datalog.record(passport_link)}"
        mongo.modify_item(item, {"transaction": transaction})
        print(transaction)
        return {"message": f"Picture passport transaction: {transaction}"}

        print("Printing QRs")
        qr_printer.generate_qrs(passport_link, transaction)
        qr_printer.print_qrs()
        os.remove(config["qr_name"])

    else:
        return {"message": "No recording in progress."}

@app.post("/esp_data")
async def receive_esp_data(data: dict):
    required_keys = {'address', 'humidity', 'temperature'}

    # Validate incoming data
    if not required_keys.issubset(data.keys()):
        raise HTTPException(status_code=400, detail="Missing required keys")



    # Get the current time
    formatted_time = datetime.now().strftime('%H:%M')
    data["timestamp"] = formatted_time

    # Add the data to MongoDB using the utility function
    mongo = mongodb_util.MongoDBUtil(config['mongo_connection_uri'], config['database_name'], "esp_data")
    item_id = mongo.add_item(data)

    return {"message": "Data added successfully", "item_id": item_id}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)