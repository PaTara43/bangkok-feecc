    // Connect to the database
    db = connect("mongodb://localhost:27017/Robonomics");

    // Create required collections
    db.createCollection("esp_data");
    db.createCollection("pictures");



    db.esp_data.insertMany(
        [
            {
                "address": "123",
                "humidity": 21,
                "temperature": 11,
                "timestamp": "16:1"
            },
            {
                "address": "123",
                "humidity": 22,
                "temperature": 12,
                "timestamp": "16:2"
            },
            {
                "address": "123",
                "humidity": 23,
                "temperature": 13,
                "timestamp": "16:3"
            },
            {
                "address": "123",
                "humidity": 24,
                "temperature": 14,
                "timestamp": "16:4"
            },
            {
                "address": "123",
                "humidity": 25,
                "temperature": 15,
                "timestamp": "16:5"
            },
            {
                "address": "123",
                "humidity": 26,
                "temperature": 16,
                "timestamp": "16:6"
            },
            {
                "address": "123",
                "humidity": 26,
                "temperature": 17,
                "timestamp": "16:7"
            },
            {
                "address": "123",
                "humidity": 25,
                "temperature": 18,
                "timestamp": "16:8"
            },
            {
                "address": "123",
                "humidity": 24,
                "temperature": 19,
                "timestamp": "16:9"
            },
            {
                "address": "123",
                "humidity": 23,
                "temperature": 20,
                "timestamp": "16:10"
            },
            {
                "address": "123",
                "humidity": 22,
                "temperature": 21,
                "timestamp": "16:11"
            },
            {
                "address": "123",
                "humidity": 21,
                "temperature": 22,
                "timestamp": "16:12"
            }
        ]
    );

