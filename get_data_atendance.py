import pandas as pd
import requests
import json
from datetime import datetime, timedelta

# Hàm xử lí thời gian
def convert_timestamp(timestamp, is_milliseconds=False):
    if is_milliseconds:
        return datetime.fromtimestamp(int(timestamp) / 1000)
    else:
        return datetime.fromtimestamp(int(timestamp))

# Hàm xử lí dữ liệu khi call API
def process_attendance_data(data, df=None):
    records = []

    for user_task_result in data["data"]["user_task_results"]:
        day = convert_timestamp(user_task_result["day"])
        employee_id = user_task_result["user_id"]
        employee_name = user_task_result["employee_name"]
        for record in user_task_result["records"]:
            check_in_time = None
            check_out_time = None
            
            # Kiểm tra và chuyển đổi thời gian check-in
            if "check_in_record" in record and record["check_in_record"]:
                check_in_record = record["check_in_record"]
                check_in_time = convert_timestamp(check_in_record["check_time"])

            # Kiểm tra và chuyển đổi thời gian check-out
            if "check_out_record" in record and record["check_out_record"]:
                check_out_record = record["check_out_record"]
                check_out_time = convert_timestamp(check_out_record["check_time"])

            if check_in_time or check_out_time:
                # Lấy ngày từ check_in_time hoặc check_out_time
                if check_in_time:
                    day = check_in_time.strftime('%Y-%m-%d')  # Lấy ngày từ check_in_time
                else:
                    day = check_out_time.strftime('%Y-%m-%d')
                records.append(
                    {
                        "day": day,
                        "employee_id": employee_id,
                        "employee_name": employee_name,
                        "check_in_time": check_in_time.strftime('%Y-%m-%d %I:%M:%S %p') if check_in_time else None,
                        "check_out_time": check_out_time.strftime('%Y-%m-%d %I:%M:%S %p') if check_out_time else None,
                    }
                )

    # Tạo DataFrame mới từ dữ liệu mới
    new_df = pd.DataFrame(records)

    # Nếu df đã tồn tại, thêm dữ liệu mới vào df cũ
    if df is not None:
        df = pd.concat([df, new_df], ignore_index=True)
    else:
        df = new_df

    return df

# Hàm để lấy dữ liệu từ ngày chỉ định đến ngày hiện tại
def get_attendance_data(start_date, end_date):
    url = "https://open.larksuite.com/open-apis/attendance/v1/user_tasks/query?employee_type=employee_id"
    payload = json.dumps({
        "check_date_from": start_date.strftime('%Y%m%d'),
        "check_date_to": end_date.strftime('%Y%m%d'),
        "user_ids": [
            "8a3g3794",
            "f74dbc4b",
            "54b99d82",
            "d76352be",
            "e8b6995c",
            "decdaaea",
            "f366de27",
            "c57cgbb2",
            "b89c3b48",
            "72dcfae1",
            "9gfe437f"
        ]
    })

    # Đọc access token từ tệp
    with open('access_token.txt', 'r') as file:
        access_token = file.read().strip()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + access_token
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = response.json()
    
    return response_dict

# Ngày bắt đầu và kết thúc cho vòng lặp
start_date = datetime(2024, 4,27)  # Ngày bắt đầu
end_date = datetime.now()  # Ngày kết thúc

# Khởi tạo DataFrame ban đầu là None
df = None

# Lặp qua mỗi ngày và lấy dữ liệu
while start_date <= end_date:
    print(f"Lấy dữ liệu cho ngày: {start_date.strftime('%Y-%m-%d')}")

    # Lấy dữ liệu chấm công
    attendance_data = get_attendance_data(start_date, start_date)

    # Xử lý dữ liệu và cập nhật DataFrame
    df = process_attendance_data(attendance_data, df)

    # Tăng ngày lên 1
    start_date += timedelta(days=1)

# Lưu DataFrame vào tệp CSV
df.to_csv("attendance_records.csv", index=False)

print(df)
