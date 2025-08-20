import random
import u6
from numbers import Number
import xtralien
import asyncio
import traceback

####### SMU and labjack data acquisition #########
async def get_sensor_data(sensor_type, ppm, smu_config, device):
    # Shared environment simulation
    # temp = round(25 + random.uniform(-1, 1), 2)
    # rh = round(50 + random.uniform(-5, 5), 2)
    temp = 0
    rh = 0

    if sensor_type == 'Resistor':
        # Real resistor Rt using SMU
        try:
            data = await run_current_vs_time(smu_config)
            hih8000 = await read_hih8000(smu_config, device)
            v_out = smu_config['v_out'].value
            resistance = v_out/data['current']
            return {'resistance': round(resistance, 9), 'temp': hih8000['temp'], 'rh': hih8000['rh']} #OK
        except Exception as e:
        # Simulated gas response curve
            print(f"SMU sweep error: {e}")
            traceback.print_exc()
            R0 = 120_000
            delta_R = 30_000
            ppm = max(ppm, 0)
            ppm_max = 1000

            resistance = R0 - delta_R * (ppm / ppm_max)
            resistance += random.uniform(-2000, 2000)
            return {'resistance': round(resistance, 2), 'temp': temp, 'rh': rh}
    
    elif sensor_type == 'Transistor':
        vgs_start = float(smu_config['v_gate_start'].value)
        vgs_stop = float(smu_config['v_gate_stop'].value)
        vgs_step = float(smu_config['v_gate_step'].value)
        if vgs_start!=vgs_stop:
            # Real transistor sweep IV using SMU
            try:
                data = await run_transistor_sweep(smu_config)
                hih8000 = await read_hih8000(smu_config, device)
                return {'vgs': data['vgs'], 'id': data['id'], 'temp': hih8000['temp'], 'rh': hih8000['rh']} #OK
            except Exception as e:
                print(f"SMU sweep error: {e}")
                traceback.print_exc()
                # Fallback to simulation in case of error
                vgs_values = []
                id_values = []
                vgs = vgs_start
                while vgs <= vgs_stop:
                    vgs = round(vgs, 4)
                    vgs_values.append(vgs)
                    id_val = 1e-6 * (vgs ** 2) + ppm * 1e-9 + random.uniform(-0.2e-6, 0.2e-6)
                    id_values.append(round(id_val, 9))
                    vgs += vgs_step
                    await asyncio.sleep(0.01)
                return {'vgs': vgs_values, 'id': id_values, 'temp': temp, 'rh': rh}
        else:
            # Real transistor I vs t using SMU
            try:
                data = await run_transistor_it(smu_config)
                hih8000 = await read_hih8000(smu_config, device)
                return {'current': data['current'], 'temp': hih8000['temp'], 'rh': hih8000['rh']} #OK
            except Exception as e:
                print(f"SMU sweep error: {e}")
                traceback.print_exc()
                I0 = 120_000
                delta_R = 30_000
                ppm = max(ppm, 0)
                ppm_max = 1000

                current = I0 - delta_R * (ppm / ppm_max)
                current += random.uniform(-2000, 2000)
                return {'current': round(current, 2), 'temp': temp, 'rh': rh}
    
    elif sensor_type == 'Diode':
        vout_start = float(smu_config['v_out_start'].value)
        vout_stop = float(smu_config['v_out_stop'].value)
        vout_step = float(smu_config['v_out_step'].value)
        if vout_start!=vout_stop:
            # Real diode sweep IV using SMU
            try:
                data = await run_diode_sweep(smu_config)
                hih8000 = await read_hih8000(smu_config, device)
                return {'vout': data['vout'], 'i_val': data['i_val'], 'temp': hih8000['temp'], 'rh': hih8000['rh']} #OK
            except Exception as e:
                print(f"SMU sweep error: {e}")
                traceback.print_exc()
                #Simulation
                vout_values = []
                i_values = []
                vout = vout_start
                while vout <= vout_stop:
                    vout = round(vout, 4)
                    vout_values.append(vout)
                    i_val = 1e-6 * (vout ** 2) + ppm * 1e-9 + random.uniform(-0.2e-6, 0.2e-6)
                    i_values.append(round(i_val, 9))
                    vout += vout_step
                    await asyncio.sleep(0.01)
                return {'vout': vout_values, 'i_val': i_values, 'temp': temp, 'rh': rh}

        else:
            # Real diode I vs time using SMU
            try:
                data = await run_current_vs_time(smu_config)
                hih8000 = await read_hih8000(smu_config, device)
                return {'current': data['current'], 'temp': hih8000['temp'], 'rh': hih8000['rh']} #OK
            except Exception as e:
            # Simulated gas response curve
                print(f"SMU sweep error: {e}")
                traceback.print_exc()
                R0 = 120_000
                delta_R = 30_000
                ppm = max(ppm, 0)
                ppm_max = 1000

                current = R0 - delta_R * (ppm / ppm_max)
                current += random.uniform(-2000, 2000)
                return {'current': round(current, 2), 'temp': temp, 'rh': rh}

    else:
        # Default fallback
        return {'temp': temp, 'rh': rh}
    
#Flow calculation for the target and carrier gases
def calculate_gas_flows(target_ppm, config):

    cylinder_ppm = config['target_gas_initialPPM']
    total_flow = config['totalFlow']

    target_flow = (target_ppm / cylinder_ppm) * total_flow
    carrier_flow = total_flow - target_flow

    return {
        'target_flow': round(target_flow, 3),
        'carrier_flow': round(carrier_flow, 3)
    }

#Calculation of the output MFC voltage
def flow_to_voltage(flow, max_flow, vref=5.0):
    v_gas = (flow / max_flow) * vref
    return round(v_gas, 3)

#Function for the MFC voltage setup
def set_analog_output(device, ao_channel, voltage):

    voltage = max(0.0, min(voltage, 5.0)) #This sets the maximum output value to 5V
    dac_value = int((voltage / 5.0) * 65535)

    if ao_channel == 'AO0':
        device.getFeedback(u6.DAC0_16(dac_value))
    elif ao_channel == 'AO1':
        device.getFeedback(u6.DAC1_16(dac_value))
    # elif ao_channel == 'AO2':
    #     device.getFeedback(u6.DAC2_16(dac_value))
    else:
        raise ValueError(f"Invalid analog output channel: {ao_channel}")

#Function to get the Analog input values
def get_analog_feedback(device, ao_channel):
    if ao_channel == 'AO0':
        return device.getAIN(0)
    elif ao_channel == 'AO1':
        return device.getAIN(1)
    else:
        raise ValueError(f"Unsupported AO channel: {ao_channel}")
    
#Function for PID control
def pid_update(target_flow, feedback_voltage, integral, prev_error, Kp, Ki, Kd, dt, max_flow):
    measured_flow = (feedback_voltage / 5.0) * max_flow
    error = target_flow - measured_flow
    integral += error * dt
    derivative = (error - prev_error) / dt
    control_flow = (Kp * error) + (Ki * integral) + (Kd * derivative) + measured_flow
    control_flow = max(0, min(control_flow, max_flow))
    voltage = flow_to_voltage(control_flow, max_flow)
    return voltage, integral, error

osr_to_delay = {
    64: 0.002, 128: 0.002, 256: 0.005, 512: 0.01,
    1024: 0.02, 2048: 0.035, 4096: 0.06, 8192: 0.12,
    16384: 0.25, 32768: 0.5
}

async def run_transistor_sweep(smu_config):
    port = smu_config['com_port'].value  
    vgs_start = float(smu_config['v_gate_start'].value)
    vgs_stop = float(smu_config['v_gate_stop'].value)
    vgs_step = float(smu_config['v_gate_step'].value)
    v_drain = float(smu_config['v_drain'].value)
    i_limit = float(smu_config['i_limit'].value)*0.001
    v_lim = float(smu_config['v_lim'].value)
    osr_value = int(smu_config['sampling'].value)
    filter_value = 10  

    delay = osr_to_delay.get(osr_value, 0.1)

    vgs_values = []
    id_values = []

    with xtralien.Device(port) as SMU:
        # For channel smu1 = drain, smu2 = gate

        # Enable channels
        SMU.smu1.set.enabled(True, response=0)
        SMU.smu2.set.enabled(True, response=0)

        # Set filters and OSR
        SMU.smu1.set.filter(filter_value, response=0)
        SMU.smu2.set.filter(filter_value, response=0)
        SMU.smu1.set.osr(osr_value, response=0)
        SMU.smu2.set.osr(osr_value, response=0)

        # Set limits
        SMU.smu1.set.limiti(i_limit, response=0)
        SMU.smu2.set.limiti(i_limit, response=0)
        SMU.smu1.set.limitv(v_lim, response=0)
        SMU.smu2.set.limitv(v_lim, response=0)

        # Set constant drain voltage
        SMU.smu1.set.voltage(v_drain, response=0)

        # Sweep gate voltage
        vgs = vgs_start
        while vgs <= vgs_stop:
            vgs_values.append(round(vgs, 4))
            SMU.smu2.set.voltage(vgs, response=0)
            await asyncio.sleep(delay)

            # Measure current at drain
            print(f'Voltage measured: {SMU.smu2.measurev()}')
            print(f'Current measured: {SMU.smu1.measurei()}')
            id_measured = float(SMU.smu1.measurei())
            id_values.append(round(id_measured, 9))

            vgs += vgs_step

        # Cleanup: turn off voltages and disable channels
        SMU.smu1.set.voltage(0, response=0)
        SMU.smu1.set.enabled(False, response=0)
        SMU.smu2.set.voltage(0, response=0)
        SMU.smu2.set.enabled(False, response=0)

    return {
        'vgs': vgs_values,
        'id': id_values,
    }

async def run_transistor_it(smu_config):
    port = smu_config['com_port'].value  
    vgs_start = float(smu_config['v_gate_start'].value)
    v_drain = float(smu_config['v_drain'].value)
    i_limit = float(smu_config['i_limit'].value)*0.001
    v_lim = float(smu_config['v_lim'].value)
    osr_value = int(smu_config['sampling'].value)
    filter_value = 10  

    delay = osr_to_delay.get(osr_value, 0.1)

    with xtralien.Device(port) as SMU:
        # For channel smu1 = drain, smu2 = gate

        # Enable channels
        SMU.smu1.set.enabled(True, response=0)
        SMU.smu2.set.enabled(True, response=0)

        # Set filters and OSR
        SMU.smu1.set.filter(filter_value, response=0)
        SMU.smu2.set.filter(filter_value, response=0)
        SMU.smu1.set.osr(osr_value, response=0)
        SMU.smu2.set.osr(osr_value, response=0)

        # Set limits
        SMU.smu1.set.limiti(i_limit, response=0)
        SMU.smu2.set.limiti(i_limit, response=0)
        SMU.smu1.set.limitv(v_lim, response=0)
        SMU.smu2.set.limitv(v_lim, response=0)

        # Set constant drain voltage
        SMU.smu1.set.voltage(v_drain, response=0)

        # Set constante gate voltage
        SMU.smu2.set.voltage(vgs_start, response=0)
        await asyncio.sleep(delay)

        # Measure current at drain
        print(f'Voltage measured: {SMU.smu2.measurev()}')
        print(f'Current measured: {SMU.smu1.measurei()}')
        id_measured = float(SMU.smu1.measurei())

        # Cleanup: turn off voltages and disable channels
        SMU.smu1.set.voltage(0, response=0)
        SMU.smu1.set.enabled(False, response=0)
        SMU.smu2.set.voltage(0, response=0)
        SMU.smu2.set.enabled(False, response=0)

    return {
        'current': id_measured,
    }

async def run_diode_sweep(smu_config):
    port = smu_config['com_port'].value
    vout_start = float(smu_config['v_out_start'].value)
    vout_stop = float(smu_config['v_out_stop'].value)
    vout_step = float(smu_config['v_out_step'].value)
    ch = smu_config['channel']
    if ch == 'CH1':
        channel = 'smu1'
    elif ch == 'CH2':
        channel = 'smu2'
    i_limit = float(smu_config['i_limit'].value)*0.001
    v_lim = float(smu_config['v_lim'].value)
    osr_value = int(smu_config['sampling'].value)
    filter_value = 10  

    delay = osr_to_delay.get(osr_value, 0.1)

    vout_values = []
    i_values = []

    with xtralien.Device(port) as SMU:

        # Enable channel
        SMU[channel].set.enabled(True, response=0)

        # Set filters and OSR
        SMU[channel].set.filter(filter_value, response=0)
        SMU[channel].set.osr(osr_value, response=0)

        # Set limits
        SMU[channel].set.limiti(i_limit, response=0)
        SMU[channel].set.limitv(v_lim, response=0)

        # Sweep gate voltage
        vout = vout_start
        while vout <= vout_stop:
            vout_values.append(round(vout, 4))
            SMU[channel].set.voltage(vout, response=0)
            await asyncio.sleep(delay)

            # Measure current
            print(f'Voltage measured: {SMU[channel].measurev()}')
            print(f'Current measured: {SMU[channel].measurei()}')
            i_measured = float(SMU[channel].measurei())
            i_values.append(round(i_measured, 9))

            vout += vout_step

        # Cleanup: turn off voltages and disable channels
        SMU[channel].set.voltage(0, response=0)
        SMU[channel].set.enabled(False, response=0)

    return {
        'vout': vout_values,
        'i_val': i_values,
    }

async def run_current_vs_time(smu_config):
    port = smu_config['com_port'].value
    if 'v_out_start' in smu_config:
        vout = float(smu_config['v_out_start'].value)
    else:
        vout = float(smu_config['v_out'].value)
    
    ch = smu_config['channel']
    if ch == 'CH1':
        channel = 'smu1'
    elif ch == 'CH2':
        channel = 'smu2'
    i_limit = float(smu_config['i_limit'].value)*0.001
    v_lim = float(smu_config['v_lim'].value)
    osr_value = int(smu_config['sampling'].value)
    filter_value = 10  

    delay = osr_to_delay.get(osr_value, 0.1)

    with xtralien.Device(port) as SMU:

        # Enable channel
        SMU[channel].set.enabled(True, response=0)

        # Set filters and OSR
        SMU[channel].set.filter(filter_value, response=0)
        SMU[channel].set.osr(osr_value, response=0)

        # Set limits
        SMU[channel].set.limiti(i_limit, response=0)
        SMU[channel].set.limitv(v_lim, response=0)

        # Sweep gate voltage
        SMU[channel].set.voltage(vout, response=0)
        await asyncio.sleep(delay)

        # Measure current
        print(f'Voltage measured: {SMU[channel].measurev()}')
        print(f'Current measured: {SMU[channel].measurei()}')
        i_measured = float(SMU[channel].measurei())

        # Cleanup: turn off voltages and disable channels
        SMU[channel].set.voltage(0, response=0)
        SMU[channel].set.enabled(False, response=0)

    return {
        'current': i_measured,
    }

async def read_hih8000(smu_config, device):
    I2C_ADDRESS = 0x27
    BYTES_TO_READ = 4
    smu = smu_config['smu']
    if smu == 'SMU1':
        SCL_PIN = 8  #EIO 0
        SDA_PIN = 9  #EIO 1
    elif smu == 'SMU2':
        SCL_PIN = 10  #EIO 2
        SDA_PIN = 11  #EIO 3
    elif smu == 'SMU3':
        SCL_PIN = 12  #EIO 4
        SDA_PIN = 13  #EIO 5
    elif smu == 'SMU4':
        SCL_PIN = 14  #EIO 6
        SDA_PIN = 15  #EIO 7

    await asyncio.sleep(0.05)
    result = device.i2c(I2C_ADDRESS, [], False, False, False, 0, SDA_PIN, SCL_PIN, 0)
    await asyncio.sleep(0.05)
    result = device.i2c(I2C_ADDRESS, [], False, False, False, 0, SDA_PIN, SCL_PIN, BYTES_TO_READ)

    data = result['I2CBytes']

    raw_humidity = ((data[0] & 0x3F) << 8) | data[1]
    humidity = (raw_humidity / 16383.0) * 100  

    raw_temp = (data[2] << 6) | (data[3] >> 2)
    temperature = (raw_temp / 16383.0) * 165 - 40
    
    return {
        'temp': round(temperature, 2),
        'rh': round(humidity, 2)
    }
