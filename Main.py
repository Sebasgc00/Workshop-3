import random as rnd

# SpaceCraft Class Definition
class SpaceCraft:
    """
    Simulates a spacecraft with basic subsystems: altitude control, payload management,
    communication status, and power constraints.

    Args:
        model (str): Name of the spacecraft
        altitude_miles (float): Altitude in miles
        payload_kg (float): Payload mass in kilograms
        comms_status (str): "Working" or "Not working"
        available_power_w (float): Available power in watts
    """

    # Constants for LEO and payload constraints
    LEO_MIN = 100
    LEO_MAX = 1200
    PAYLOAD_MIN = 1000
    PAYLOAD_MAX = 10000
    POWER_MIN = 600
    POWER_MAX = 1000


    def __init__(self, model, altitude_miles, payload_kg, comms_status, available_power_w):
        self.model = model
        self.altitude_miles = altitude_miles
        self.payload_kg = payload_kg
        self.comms_status = comms_status
        self.available_power = available_power_w
        self.status = "Idle"



    def report_status(self):
        print(f"\n--- {self.model} Spacecraft Report ---")
        print(f"Status: {self.status}")
        print(f"Altitude: {self.altitude_miles} miles")
        print(f"Payload: {self.payload_kg} kg")
        print(f"Comms: {self.comms_status}")
        print(f"Available Power: {self.available_power} W")
        

    def control_altitude_miles(self, new_altitude_mi):
        REQUIRED_POWER = 200
        if self.available_power < REQUIRED_POWER:
            self.status = "Altitude Error: Low Power"
            print(f"[{self.model}] Cannot adjust altitude — Need {REQUIRED_POWER} W, have {self.available_power} W")
            return
        if self.LEO_MIN <= new_altitude_mi <= self.LEO_MAX:
            self.altitude_miles = new_altitude_mi
            self.status = "Altitude Adjusted"
            print(f"[{self.model}] Altitude adjusted to {self.altitude_miles} miles")
        else:
            self.status = "Altitude Error"
            print(f"[{self.model}] Altitude {new_altitude_mi} miles is outside LEO range!")

    def operate_payload(self):
        REQUIRED_POWER = 300
        if self.available_power < REQUIRED_POWER:
            self.status = "Payload Error: Low Power"
            print(f"[{self.model}] Cannot operate payload — Need {REQUIRED_POWER} W, have {self.available_power} W")
            return
        if self.PAYLOAD_MIN <= self.payload_kg <= self.PAYLOAD_MAX:
            self.status = "Payload Operating"
            print(f"[{self.model}] Payload operational with {self.payload_kg} kg")
        else:
            self.status = "Payload Error"
            print(f"[{self.model}] Payload {self.payload_kg} kg out of allowed range ({self.PAYLOAD_MIN}-{self.PAYLOAD_MAX} kg)!")

    def send_data(self):
        REQUIRED_POWER = 100
        if self.available_power < REQUIRED_POWER:
            self.status = "Comms Error: Low Power"
            print(f"[{self.model}] Cannot send data — Need {REQUIRED_POWER} W, have {self.available_power} W")
            return
        if self.comms_status == "Working":
            self.status = "Transmitting"
            print(f"[{self.model}] Data transmitted to Earth")
        else:
            self.status = "Comms Error"
            print(f"[{self.model}] Cannot transmit — Comms not working")
    
    def power_system(self):
        if self.POWER_MIN <= self.available_power <= self.POWER_MAX:
            P_S = "POWER BY BATERY" # The batteries are working normally.
        elif self.available_power<self.POWER_MIN:
            P_S = "EMERG LOW PWR; POWER BY SUN PANELS" 
        else:
            P_S = "FAILURE IN DATA"
        print(f"[{self.model}] POWER STATUS: {P_S}")
        return P_S

# Eventos aleatorios 

class eventosaleatorios:
        def __init__(self, SpaceCraft):
            self.SpaceCraft = SpaceCraft
            self.sistema_alterno_activo = False
        def eclipse_solar(self):
            print("Solar energy lost for eclipse")
            energia_actual = int(self.SpaceCraft.available_power)
            energia_reducida =max(0, energia_actual - 300)
            self.SpaceCraft.available_power = (energia_reducida)
            print(f"Energy reduced to {self.SpaceCraft.available_power} W")

# Estado del sistema de comunicacion
            if energia_reducida >= 800:
                self.SpaceCraft.comms = "Working"
                print("Comms: Working")
            elif energia_reducida < 800:
                print("Alert: Comms disable")

            if energia_reducida < 800 and not self.sistema_alterno_activo:
                self.activar_sistema_alterno()

        def activar_sistema_alterno(self):
            print(f"Activating alternate energy system of {self.SpaceCraft.model}")
            energia_extra = 200  # Cantidad de energía que aporta el sistema alterno
            self.SpaceCraft.available_power += energia_extra
            self.sistema_alterno_activo = True
            print(f"Power restored to {self.SpaceCraft.available_power} W")

        # Actualizar estado de comunicación después de activar sistema alterno
            if self.SpaceCraft.available_power >= 800:
                self.SpaceCraft.comms = "Working"
                print("Communication restored")
            else:
                print("Insufficient power, communication remains disabled")
