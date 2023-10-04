from timelength import TimeLength

test_cases = [
    ["5m", 300],
    ["10 days and um 3 sec", 864003],
    ["7 sec", 7],
    ["2 weeks", 1209600],
    ["qoithewqt", 0],
]

for test, expected in test_cases:
    length = TimeLength(test)
    print(f"Valid: {bool(length.total_seconds)}")
    print(f"Total Seconds: {length.total_seconds}")

    assert length.total_seconds == expected

print("All Tests Successfull!")
