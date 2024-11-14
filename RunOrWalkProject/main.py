from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Pydantic model
class Activity(BaseModel):
    id: int
    username: str
    activity: str
    date: str
    time: str
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float

# Veritabanı bağlantısını sağlayan bir fonksiyon
def get_db_connection():
    conn = sqlite3.connect('activities.db')
    conn.row_factory = sqlite3.Row
    return conn

# GET: Tüm kayıtları al
@app.get("/activities/", response_model=list[Activity])
def get_activities():
    conn = get_db_connection()
    activities = conn.execute('SELECT * FROM activities').fetchall()
    conn.close()
    return [dict(row) for row in activities]

# GET: Belirli bir kaydı ID ile al
@app.get("/activities/{activity_id}", response_model=Activity)
def get_activity(activity_id: int):
    conn = get_db_connection()
    activity = conn.execute('SELECT * FROM activities WHERE id = ?', (activity_id,)).fetchone()
    conn.close()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return dict(activity)

# POST: Yeni kayıt ekle
@app.post("/activities/", response_model=Activity)
def create_activity(activity: Activity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activities (username, activity, date, time, acceleration_x, acceleration_y, acceleration_z, gyro_x, gyro_y, gyro_z)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (activity.username, activity.activity, activity.date, activity.time, 
          activity.acceleration_x, activity.acceleration_y, activity.acceleration_z, 
          activity.gyro_x, activity.gyro_y, activity.gyro_z))
    conn.commit()
    activity.id = cursor.lastrowid
    conn.close()
    return activity

# PUT: Belirli bir kaydı güncelle
@app.put("/activities/{activity_id}", response_model=Activity)
def update_activity(activity_id: int, activity: Activity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE activities
        SET username = ?, activity = ?, date = ?, time = ?, acceleration_x = ?, 
            acceleration_y = ?, acceleration_z = ?, gyro_x = ?, gyro_y = ?, gyro_z = ?
        WHERE id = ?
    ''', (activity.username, activity.activity, activity.date, activity.time,
          activity.acceleration_x, activity.acceleration_y, activity.acceleration_z,
          activity.gyro_x, activity.gyro_y, activity.gyro_z, activity_id))
    conn.commit()
    conn.close()
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity.id = activity_id
    return activity

# DELETE: Belirli bir kaydı sil
@app.delete("/activities/{activity_id}")
def delete_activity(activity_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
    conn.commit()
    conn.close()
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {"message": "Activity deleted successfully"}