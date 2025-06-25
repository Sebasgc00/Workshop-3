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


# SUBSYSTEM: Altitude Control

class AltitudeControlSystem:
    def __init__(self, spacecraft):
        self.spacecraft = spacecraft

    def adjust_altitude(self, target_altitude, torque_input, angular_velocity):
        REQUIRED_POWER = 200
        print(f"\n[{self.spacecraft.model} - AltitudeControl] Attempting altitude change ")

        if self.spacecraft.available_power < REQUIRED_POWER:
            return {"status": "Failed", "reason": "Low Power"}

        if not (self.spacecraft.LEO_MIN <= target_altitude <= self.spacecraft.LEO_MAX):
            return {"status": "Failed", "reason": "Target altitude out of bounds"}

        # Simulate control based on inputs (simple placeholder)
        adjustment_effectiveness = torque_input * angular_velocity

        if adjustment_effectiveness < 10:
            return {"status": "Failed", "reason": "Insufficient torque/angular velocity"}

        # Apply adjustment
        self.spacecraft.altitude_miles = target_altitude
        self.spacecraft.available_power -= REQUIRED_POWER
        return {"status": "Success", "new_altitude": target_altitude}

# SUBSYSTEM: Communication System

class CommsSystem:
    def __init__(self, spacecraft):
        self.spacecraft = spacecraft
        self.payload_data = "Payload data stream"

        # Generalized telemetry as a placeholder dictionary
        self.telemetry = {
            "sensor_1": "value_1",
            "sensor_2": "value_2",
            "status_flag": "OK"
        }

    def send_command(self, command):
        if self.spacecraft.available_power < 100:
            return {"status": "Failed", "reason": "Insufficient Power"}

        if self.spacecraft.comms_status != "Working":
            return {"status": "Failed", "reason": "Comms not working"}

        self.spacecraft.available_power -= 100
        return {"status": "Command Executed", "command": command}

    def transmit_payload(self):
        if self.spacecraft.comms_status == "Working":
            return {"status": "Data Sent", "payload": self.payload_data}
        else:
            return {"status": "Failed", "reason": "Comms not working"}

    def send_telemetry(self):
        if self.spacecraft.comms_status == "Working":
            # Simulate changing telemetry values for general use
            self.telemetry = {
                "sensor_1": rnd.choice(["nominal", "high", "low"]),
                "sensor_2": rnd.randint(0, 100),
                "status_flag": rnd.choice(["OK", "WARNING", "FAIL"])
            }
            return {"status": "Telemetry Sent", "data": self.telemetry}
        else:
            return {"status": "Failed", "reason": "Comms failure"}

# SUBSYSTEM: Energy system

class SistemaEnergia:
    def __init__(self, spacecraft):
        self.spacecraft = spacecraft
        self.energia_origen = "Bateria"

    def evaluar_energia(self):
        if self.spacecraft.available_power >= SpaceCraft.POWER_MIN:
            self.energia_origen = "Bateria"
            print(f"[{self.spacecraft.model}] Energia suficiente: operando con batería")
        elif 0 < self.spacecraft.available_power < SpaceCraft.POWER_MIN:
            self.energia_origen = "Panel Solar"
            print(f"[{self.spacecraft.model}] Energía baja: usando paneles solares")
            self.desactivar_sistemas()
        else:
            print(f"[{self.spacecraft.model}] Falla crítica: sin energía disponible")
            self.desactivar_sistemas()

    def desactivar_sistemas(self):
        self.spacecraft.status = "Sistemas desactivados por baja energía"
        self.spacecraft.comms_status = "Not Working"
        print(f"[{self.spacecraft.model}] TODOS LOS SISTEMAS DESACTIVADOS")


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

# Create Spacecrafts

# 1. Satellite with enough power and all systems within range
SC1 = SpaceCraft("Apolo", rnd.randint(80,1500), rnd.randint(900,12000), "Working", rnd.randint(0,1100))

# 2. Satellite with altitude outside the LEO range
SC2 = SpaceCraft("Starship", rnd.randint(80,1500), rnd.randint(900,12000), "Working", rnd.randint(0,1100))

# 3. Satellite with payload outside the allowed range
SC3 = SpaceCraft("Voyager-X", rnd.randint(80,1500), rnd.randint(900,12000), "Working", rnd.randint(0,1100))

# 4. Satellite without sufficient power to operate the payload
SC4 = SpaceCraft("LowPowerSat",rnd.randint(80,1500), rnd.randint(900,12000), "Working", rnd.randint(0,1100))

# 5. Satellite with damaged communication system
SC5 = SpaceCraft("MiniSat", rnd.randint(80,1500), rnd.randint(900,12000), "Not Working", rnd.randint(0,1100))


# Reports subsystems
SpaceCrafts= [SC1, SC2, SC3, SC4, SC5]

def execute(list):
    for i in list:

        i.report_status()

        print("\n--- GENERAL OPERATIONS ---")

        i.control_altitude_miles(rnd.randint(0, 1000))
        i.power_system()
        i.operate_payload()
        i.send_data() 

        print("\n--- ALTITUDE OPERATIONS ---")

        altitude_system = AltitudeControlSystem(i)
        result =altitude_system.adjust_altitude(target_altitude=rnd.randint(0,500),torque_input=rnd.randint(1,10), angular_velocity=rnd.randint(1,5))
        print("\n Altitude Adjustment   Result:", result)

        print("\n--- COMMS OPERATIONS ---")

        comms_system = CommsSystem(i)
        command_result = comms_system.send_command("Activate Camera")
        payload_result = comms_system.transmit_payload()
        telemetry_result = comms_system.send_telemetry()

        print("\n Command Result:", command_result)
        print("Payload Transmission:", payload_result)
        print("Telemetry:", telemetry_result)

        print("\n--- ENERGY OPERATION ---")

        sistema_energia = SistemaEnergia(i)
        sistema_energia.evaluar_energia()
        i.report_status()

        print("\n--- CHARGE OPERATION ---")

        carga = CargaUtil(rnd.randint(0,10000))
        print(carga.estado_carga())
        carga.liberar_carga(1000)
        print(carga.estado_carga())
        carga.liberar_carga(4500)  # Intento fallido, no hay suficiente
        print(carga.estado_carga())


        print("\n--- ALEATORY EVENTS ---")

        evento = eventosaleatorios(i)
        evento.eclipse_solar()
        print("\n" + "-"*50 + "\n")


        

execute(SpaceCrafts)