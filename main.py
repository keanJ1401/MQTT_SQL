import paho.mqtt.client as mqtt
from sqlalchemy import create_engine, func, join, update
from sqlalchemy import Column, String, Integer, TIMESTAMP, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# SQL ORM
db = create_engine('postgresql://postgres:user@35.221.141.147/database')

base = declarative_base()


class Home(base):
    __tablename__ = 'home'
    sensor_id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('devices.device_id'))
    type = Column(String)
    name = Column(String)

    def __init__(self, device_id, type, name):
        self.device_id = device_id
        self.type = type
        self.name = name


class Devices(base):
    __tablename__ = 'devices'
    device_id = Column(Integer, primary_key=True)
    name = Column(String)
    ip_device = Column(String)
    parent_id = Column(String, nullable=True)
    up_time = Column(TIMESTAMP, nullable=True)
    location = Column(String)

    def __init__(self, device_id, name, ip_device, location, parent_id=None, up_time=None):
        self.device_id = device_id
        self.name = name
        self.ip_device = ip_device
        self.parent_id = parent_id
        self.up_time = up_time
        self.location = location

    def json(self):
        return {'device_id': self.device_id, 'name': self.name, 'ip_device': self.ip_device, 'parent_id': self.parent_id, 'up_time': self.up_time, 'location': self.location}

    @classmethod
    def get_by_device_id(cls, device_id: int):
        device_data = session.query(cls).filter_by(device_id=device_id).first().json()
        session.rollback()
        return device_data

    @classmethod
    def get_all_device(cls):
        query = session.query(cls)
        devices = [i.json() for i in query]
        return devices

    @classmethod
    def add(cls, device_id, name, ip_device='NaN', parent_id=None, up_time=None, location= 'NaN'):
        new_devices = cls(device_id=device_id, name=name, ip_device=ip_device, location=location, parent_id=parent_id, up_time=up_time)
        session.add(new_devices)
        session.commit()
        session.rollback()


class Sensors(base):
    __tablename__ = 'sensors'
    id = Column(Integer, primary_key=True)
    sensor_id = Column(Integer, ForeignKey('sensors.sensor_id'))
    value = Column(JSON)
    time = Column(TIMESTAMP)

    def __init__(self, sensor_id, value, time):
        self.sensor_id = sensor_id
        self.value = value
        self.time = time

    def json(self):
        return {'sensor_id': self.sensor_id, 'value': self.value, 'time': self.time.strftime("%Y-%m-%d %H:%M:%S")}

    @classmethod
    def get_by_sensor_id(cls, sensor_id: int):
        sensor_data = session.query(Sensors).filter_by(sensor_id=sensor_id).order_by(cls.id.desc()).first().json()
        session.rollback()
        return sensor_data

    @classmethod
    def get_last_value(cls):
        last_date = session.query(Sensors.sensor_id, func.max(Sensors.time).label('value_up_to_date')).group_by(
            Sensors.sensor_id).subquery()
        query = session.query(Sensors).join(
            last_date, Sensors.time == last_date.c.value_up_to_date).order_by(Sensors.sensor_id).all()
        last_value = [i.json() for i in query]
        session.rollback()
        return last_value

    @classmethod
    def add(cls, sensor_id, value, time=datetime.now()):
        new_value = cls(sensor_id=sensor_id, value=value, time=time.strftime("%Y-%m-%d %H:%M:%S"))
        session.add(new_value)
        session.commit()
        session.rollback()
        return new_value

    @classmethod
    def update(cls, sensor_id, value, time=datetime.now()):
        stmt = update(cls).where(cls.sensor_id == sensor_id).values(
            value=value, time=time.strftime("%Y-%m-%d %H:%M:%S")).execution_options(synchronize_session="fetch")
        result = session.execute(stmt)
        session.rollback()
        return result


class Actuators(base):
    __tablename__ = 'actuators'
    sensor_id = Column(Integer, ForeignKey('sensors.sensor_id'), primary_key=True)
    state = Column(Integer)
    time = Column(TIMESTAMP)

    def __init__(self, sensor_id, state, time):
        self.sensor_id = sensor_id
        self.state = state
        self.time = time

    def json(self):
        return {'sensor_id': self.sensor_id, 'state': self.state, 'time': self.time.strftime("%Y-%m-%d %H:%M:%S")}

    @classmethod
    def get_by_sensor_id(cls, sensor_id: int):
        sensor_date = session.query(Actuators).filter_by(sensor_id=sensor_id).first().json()
        session.rollback()
        return sensor_date

    @classmethod
    def get_last_state(cls):
        last_date = session.query(
            Actuators.sensor_id,func.max(Actuators.time).label('state_up_to_date')).group_by(
            Actuators.sensor_id).subquery()
        query = session.query(Actuators).join(last_date, Actuators.time == last_date.c.state_up_to_date).order_by(
            Actuators.sensor_id).all()
        last_state = [i.json() for i in query]
        session.rollback()
        return last_state

    @classmethod
    def add(cls, sensor_id, state, time=datetime.now()):
        new_state = cls(sensor_id=sensor_id, state=state, time=time.strftime("%Y-%m-%d %H:%M:%S"))
        session.add(new_state)
        session.commit()
        session.rollback()
        return new_state

    @classmethod
    def update(cls, sensor_id, state, time=datetime.now()):
        stmt = update(cls).where(cls.sensor_id == sensor_id).values(
            state=state, time=time.strftime("%Y-%m-%d %H:%M:%S")).execution_options(synchronize_session="fetch")
        result = session.execute(stmt)
        session.rollback()
        return result


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

rs = Actuators.add(2, 1)
print(rs)
data = Actuators.get_last_state()
for d in data:
    print(d)
'''
# Create
nodemcu_esp8266 = Devices(device_id=5, name="ESP8266", ip_device="NaN", parent_id=None, up_time=None, location="NaN")
session.add(nodemcu_esp8266)
session.commit()

# Read
devices = session.query(Devices)
for device in devices:
    print(device.name)

# Update
nodemcu_esp8266.name = 'ESP32'
session.commit()

# Delete
session.delete(nodemcu_esp8266)
session.commit()
'''

'''
# Connection success callback
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe('sensor/#')


# Message receiving callback
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()

# Specify callback function
client.on_connect = on_connect
client.on_message = on_message

# Establish a connection
client.connect('192.168.0.101', 1883, 60)
client.loop_forever()
'''

