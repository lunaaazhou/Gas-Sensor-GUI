from nicegui import ui,app
import asyncio
import matplotlib
import random
import csv
from pathlib import Path
from logic import get_sensor_data, calculate_gas_flows, flow_to_voltage, set_analog_output, pid_update, get_analog_feedback
import u6
import serial.tools.list_ports


# Main GUI class
class GasSensorApp:
    def __init__(self, labjack,com_ports):
        self.running = False
        self.labjack = labjack
        labjack_status = labjack is not None  
        self.available_ports = [port.device for port in com_ports]
        dark = ui.dark_mode()
        def close_app():
            if self.labjack is not None:
                print("Closing LabJack connection...")
                self.labjack.close()
            app.shutdown()
        with ui.row().classes('w-full'):
            with ui.column().style('align-items: center; margin-top: 0px;'):
                with ui.row().style('gap: 20px;'):
                    ui.switch('Dark mode').bind_value(dark)
                    ui.button('shutdown', on_click=close_app, color='negative')
                ui.label('Gas Sensor Characterization Platform').style('font-size: 22px; font-weight: bold; margin-bottom: 0px;').classes('text-center')
                
                with ui.row().style('gap: 20px;'):
                    with ui.column().style('align-items: center; margin-top: 30px; gap: 10px;'):
                        # Start and stop buttons
                        with ui.row().style('gap: 20px;'):
                            def handle_start_click():
                                self.start_experiment()
                                #self.tabs.set_value('Results')

                            self.start_btn = ui.button('Start', on_click=handle_start_click).style('width: 120px;')
                            self.stop_btn = ui.button('Stop', on_click=self.stop_experiment).style('width: 120px;')
                            self.stop_btn.disable()

                        # Status indicators
                        self.status_label = ui.label('Status: Idle').style('margin-top: 10px; font-weight: bold;')
                        self.labjack_label = ui.label().style('margin-top: 5px;')

                        if labjack_status:
                            self.labjack_label.set_text("LabJack: Connected")
                            self.labjack_label.style("color: green")
                        else:
                            self.labjack_label.set_text("LabJack: Disconnected")
                            self.labjack_label.style("color: red")
            ui.space()
            with ui.column().style('align-items: center; margin-top: 0px;'):
                ui.label('Error List').style('font-size: 18px; font-weight: bold; margin-top: 0px; margin-left: 0px;')
                with ui.card().style('margin-bottom: 0px; width: 500px;'):
                    self.error_list = ui.list().props('dense separator')

        with ui.tabs() as self.tabs:
            setupTab = ui.tab('Environment Setup')
            testTab = ui.tab('Test Setup')
            smuTab = ui.tab('Gas Sensors Setup')
            resultsTab = ui.tab('Results')
        
        with ui.tab_panels(self.tabs, value=setupTab):
            #MFC Setup Tab
            with ui.tab_panel(setupTab):
                with ui.row():
                    with ui.column():
                        ui.label('MFC Setup').style('font-size: 18px; font-weight: bold; margin-top: 0px; margin-left: 0px;')
                        with ui.card():
                            with ui.row().style('justify-content: space-between; width: 1350px;'):
                                ui.label('Gas Name').style('margin-left: 320px; width: 140px; font-weight: bold;')
                                ui.label('Analog Output').style('margin-left: -20px; width: 140px; font-weight: bold; ')
                                ui.label('Full Scale Flow (sccm)').style('margin-left: -20px; width: 160px; font-weight: bold; ')
                                ui.label('Cylinder Concentration (ppm)').style('width: 200px; font-weight: bold; margin-left: 0px')
                            for mfc_label in ['Target Gas', 'Carrier Gas', 'Interfering Gas']:
                                with ui.card().style('margin-top: -10px; margin-bottom: 0px; width: 1380px; font-size:15px;'):  # Wider card for table layout
                                # Build one row like a table
                                    with ui.row().classes('items-center').style('gap: 170px;'):
                                        # Column 1: Gas Name Label
                                        ui.label(mfc_label).style('width: 150px; font-weight: bold;')
                                        # Column 2: Gas Dropdown (menu for gas)
                                        setattr(
                                            self,
                                            f'{mfc_label.lower().replace(" ", "_")}_gasType',
                                            ui.select(
                                                options=['Air', 'CO2'],
                                                value='Air',
                                            ).style('width: 100px;')
                                        )
                                        # Column 3: Analog Output Dropdown
                                        setattr(
                                            self,
                                            f'{mfc_label.lower().replace(" ", "_")}_analogOut',
                                            ui.select(
                                                options=['AO0', 'AO1', 'AO2', 'None'],
                                                value='None',
                                            ).style('width: 100px;')
                                        )
                                        # Column 4: Full Scale Flow (sccm)
                                        setattr(
                                            self,
                                            f'{mfc_label.lower().replace(" ", "_")}_maxflow',
                                            ui.number(
                                                value=0, min=0, max=10000, step=1
                                            ).style('width: 130px;')
                                        )
                                        # Column 5: Cylinder Concentration (ppm)
                                        setattr(
                                            self,
                                            f'{mfc_label.lower().replace(" ", "_")}_initialppm',
                                            ui.number(
                                                value=0, min=0, max=10000, step=1
                                            ).style('width: 160px;')
                                        )

                            for mfc_label in ['Total Flow Rate (sccm)']:
                                with ui.card().style('margin-top: 20px; margin-left:0px; margin-bottom: 0px; width: 1380px; font-size:15px;'):  # Wider card for table layout
                                # Build one row like a table
                                    with ui.row().classes('items-center').style('gap: 170px;'):
                                        
                                        # Column 1: Total Flow Rate Label
                                        ui.label(mfc_label).style('width: 150px; font-weight: bold;')
                                        # Total Flow Rate
                                        setattr(
                                            self,
                                            f'totalflow',
                                            ui.number(
                                                value=1000, min=0, max=10000, step=1
                                            ).style('width: 130px;')
                                        )

                        ui.label('Humidity Control').style('font-size: 18px; font-weight: bold; margin-top: 0px;')
                        with ui.card().style('margin-bottom: 0px; width: 380px;'):
                            with ui.row():
                                ui.label('Humidity Set Point (%RH)').style('width: 160px; font-size:15px; font-weight: bold; margin-top:10px;')
                                self.humidity_set_point = ui.number(value=50, min=0, max=100, step=1).style('width: 100px;')
            #Test Setup Tab
            with ui.tab_panel(testTab):
                with ui.row():
                    with ui.column():
                        # Section: timing parameters for stabilization and recovery
                        ui.label('Timing Setup').style('font-size: 18px; font-weight: bold; margin-top: 10px;')
                        with ui.card().style('margin-bottom: 10px; width: 350px;'):
                            with ui.row():
                                ui.label('Stabilization Time (m)').style('width: 150px;')
                                self.stab_time = ui.number(value=5, min=0, max=300, step=1).style('width: 100px;') # Stabilization time
                            with ui.row():
                                ui.label('Exposure Time (m)').style('width: 150px;')
                                self.expo_time = ui.number(value=10, min=0, max=300, step=1).style('width: 100px;') # Exposure time
                            with ui.row():
                                ui.label('Recovery Time (m)').style('width: 150px;')
                                self.rec_time = ui.number(value=5, min=0, max=300, step=1).style('width: 100px;') # Recovery time

                        ui.label('Sampling Frequency (Hz)').style('font-size: 18px; font-weight: bold; margin-top: 10px;')
                        with ui.card().style('margin-bottom: 10px; width: 350px;'):
                            with ui.row():
                                self.sample_freq = ui.number(value=10, min=0, max=1000, step=1).style('width: 100px;')
                    with ui.column():
                        #Section: test type
                        ui.label('Test Type and Parameters').style('font-size: 18px; font-weight: bold; margin-top: 10px;')
                        with ui.card().style('margin-bottom: 10px; width: 350px;'):
                            self.test_type = ui.radio(['Linear', 'Pulse', 'Custom'], value='Linear') # Test selection
                            self.cond_params = ui.column() # Parameters update 
                            test_types = ['Linear', 'Pulse', 'Custom']
                            self.test_type.on('update:model-value', lambda e: self.update_test_type_params(test_types[e.args]))
                            self.update_test_type_params(self.test_type.value)
                    #Test Preview Plot and simulated real-time outputs
                    with ui.column():
                        ui.label('Test Preview Plot').style('font-size: 18px; font-weight: bold; margin-top: 10px;')
                        with ui.card().style('margin-bottom: 10px; width: 650px; height: 500px;'):
                            ui.button('Show Preview', on_click=self.update_preview_plot).style('margin-top: 10px;')
                            self.preview_plot = ui.echart({
                                'xAxis': {
                                    'type': 'value',
                                    'name': 'Time (m)',
                                    'axisLabel': {'formatter': '{value}'}
                                },
                                'yAxis': {'type': 'value', 'name': 'ppm'},
                                'series': [{
                                    'type': 'line',
                                    'step': 'start',
                                    'data': [],
                                    'name': 'PPM',
                                    'areaStyle': {}  
                                }],
                                'tooltip': {'trigger': 'axis'}
                            }).style('width: 600px; height: 500px;')
            #SMU Setup Tab
            with ui.tab_panel(smuTab):
                with ui.row():
                    with ui.column():                        
                        #Section: Sensor type
                        ui.label('Gas Sensor Type').style('font-size: 18px; font-weight: bold; margin-top: 0px;')
                        with ui.card().style('margin-bottom: 10px; width: 350px;'):
                            self.sensor_type = ui.radio(['Resistor', 'Transistor', 'Diode'], value='Resistor') # Sensor selection
                    
                        with ui.card().style('width: 400px; height: 200px;'):
                            ui.label('Outputs').style('font-size: 18px; font-weight: bold; margin-bottom: 15px;').classes('text-center')
                            # Progress bar
                            ui.label('Experiment Progress').style('font-weight: bold; margin-top: 20px;')
                            self.progress_bar = ui.linear_progress()
                    with ui.column():
                        # Section: SMU configuration
                        ui.label('SMU Setup').style('font-size: 18px; font-weight: bold; margin-top: 0px;')
                        self.smu_card = ui.card().style('margin-bottom: 10px; width: 1070px;')
                        self.sensor_type.on('update:model-value', lambda _: self.update_smu_setup_based_on_sensor_type())
                        self.update_smu_setup_based_on_sensor_type()
                        
            #Results Tab
            with ui.tab_panel(resultsTab):
                self.results_section = ui.row()

    # Updates the panel depending on the selected test type
    @ui.refreshable
    def update_test_type_params(self, test_type):
        self.cond_params.clear()
        if test_type == 'Linear':
            with self.cond_params:
                ui.label('Linear Sweep Parameters').style('font-weight: bold;')
                self.lin_start = ui.number(value=0, min=0, max=10000, step=1, label='Start ppm').style('width: 150px;')
                self.lin_stop = ui.number(value=1000, min=0, max=10000, step=1, label='Stop ppm').style('width: 150px;')
                self.lin_step = ui.number(value=200, min=0.1, max=1000, step=0.1, label='Step ppm').style('width: 150px;')
        elif test_type == 'Pulse':
            with self.cond_params:
                ui.label('Pulse Test Parameters').style('font-weight: bold;')
                self.pulse_ppm = ui.number(value=500, min=0, max=10000, step=1, label='Pulse ppm').style('width: 150px;')
                self.pulse_count = ui.number(value=5, min=1, max=100, step=1, label='Pulse Count').style('width: 150px;')
        elif test_type == 'Custom':
            with self.cond_params:
                ui.label('Custom Test Parameters').style('font-weight: bold;')
                self.custom_ppm_list = ui.textarea(placeholder='Comma separated ppm values, e.g. 400,200,600').style('width: 300px; height: 130px;')
    
    def update_smu_setup_based_on_sensor_type(self):
        current_ranges = {
            'Autorange': 1,  # handled separately
            '200 mA': 0.2,
            '20 mA': 0.02,
            '2 mA': 0.002,
            '200 µA': 0.0002,
            '20 µA': 0.00002
        }
        unit_scaling = {
            '200 mA': ('mA', 1e3),
            '20 mA': ('mA', 1e3),
            '2 mA': ('mA', 1e3),
            '200 µA': ('µA', 1e6),
            '20 µA': ('µA', 1e6)
        }
        sampling_rates = [str(v) for v in [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]]
        self.smu_card.clear()
        self.sensor_config = []

        with self.smu_card:
            with ui.row().classes('font-bold'):
                ui.markdown('Enable').style('width: 45px;')
                ui.markdown('SMU-CH(s)').style('width: 90px;')
                ui.markdown('COM port').style('width: 75px;')
                ui.markdown('Name').style('width: 80px;')
                if self.sensor_type.value == 'Transistor':
                    ui.markdown('V<sub>D</sub> [CH1]').style('width: 62px;')
                    ui.markdown('V<sub>G</sub> [CH2] Start').style('width: 62px;')
                    ui.markdown('V<sub>G</sub> [CH2] Stop').style('width: 62px;')
                    ui.markdown('V<sub>G</sub> [CH2] Step').style('width: 62px;')
                    ui.markdown('V Lim (V)').style('width: 65px;')
                elif self.sensor_type.value == 'Resistor':
                    ui.markdown('V Out').style('width: 60px;')
                    ui.markdown('V Lim (V)').style('width: 60px;')
                elif self.sensor_type.value == 'Diode':
                    ui.markdown('V Out Start').style('width: 62px;')
                    ui.markdown('V Out Stop').style('width: 62px;')
                    ui.markdown('V Out Step').style('width: 62px;')
                    ui.markdown('V Lim (V)').style('width: 65px;')
                ui.markdown('I Range').style('width: 90px;')
                ui.markdown('I Lim (mA)').style('width: 90px;')
                ui.markdown('Sampling Rate').style('width: 70px;')

            self.sensor_config = []

            if self.sensor_type.value == 'Transistor':
                for i in range(0, 8, 2):
                    smu = f"SMU{(i//2)+1}"
                    smu_ch1 = f"SMU{(i//2)+1}-CH1"
                    smu_ch2 = f"SMU{(i//2)+1}-CH2"
                    with ui.row().style('margin-bottom: 4px; align-items: center;'):
                        enabled = ui.checkbox(value=False)
                        smu_label = ui.label(f'{smu_ch1}, {smu_ch2}').style('width: 100px; font-weight: bold;')
                        com_port = ui.select(options=self.available_ports, value=self.available_ports[0] if self.available_ports else None).style('width: 70px;')
                        sensor_name = ui.input(placeholder=f'Sensor {i//2+1}', value=f'Sensor {i//2+1}').style('width: 100px;')

                        v_drain = ui.number(value=1.0, min=-10, max=10, step=0.1).style('width: 60px;')
                        v_gate_start = ui.number(value=0.0, min=-10, max=10, step=0.1).style('width: 60px;')
                        v_gate_stop = ui.number(value=2.0, min=-10, max=10, step=0.1).style('width: 60px;')
                        v_gate_step = ui.number(value=0.5, min=0.00001, max=1, step=0.01).style('width: 60px;')

                        v_lim = ui.number(value=10.5, min=0, max=10.5, step=0.1).style('width: 60px;')

                        i_range_select = ui.select(options=list(current_ranges.keys()), value='200 mA').style('width: 90px;')

                        i_limit = ui.number(value=225, min=0, max=225, step=1).style('width: 80px;')

                        sampling = ui.select(options=sampling_rates, value='1024').style('width: 70px;')

                        self.sensor_config.append({
                            'enabled': enabled,
                            'name': sensor_name,
                            'smu': smu,
                            'channel': 'CH1-CH2',
                            'com_port': com_port,
                            'v_drain': v_drain,
                            'v_gate_start': v_gate_start,
                            'v_gate_stop': v_gate_stop,
                            'v_gate_step': v_gate_step,
                            'v_lim': v_lim,
                            'i_range': i_range_select,
                            'i_limit': i_limit,
                            'sampling': sampling
                        })
            elif self.sensor_type.value == 'Resistor':
                for i in range(8):
                    smu = f"SMU{(i//2)+1}"
                    ch = f"CH{(i%2)+1}"
                    with ui.row().style('margin-bottom: 4px; align-items: center;'):
                        enabled = ui.checkbox(value=False)
                        smu_label = ui.label(f'{smu}-{ch}').style('width: 100px; font-weight: bold;')
                        com_port = ui.select(options=self.available_ports, value=self.available_ports[0] if self.available_ports else None).style('width: 70px;')
                        sensor_name = ui.input(placeholder=f'Sensor {i+1}', value=f'Sensor {i+1}').style('width: 95px;')
                        v_out = ui.number(value=0.0, min=-10, max=10, step=0.1).style('width: 55px;')
                        v_lim = ui.number(value=10.5, min=0, max=10.5, step=0.1).style('width: 55px;')

                        i_range_select = ui.select(options=list(current_ranges.keys()), value='200 mA').style('width: 90px;')

                        i_limit = ui.number(value=225, min=0, max=225, step=1).style('width: 80px;')

                        sampling = ui.select(options=sampling_rates, value='1024').style('width: 70px;')

                        self.sensor_config.append({
                            'enabled': enabled,
                            'name': sensor_name,
                            'smu': smu,
                            'channel': ch,
                            'com_port': com_port,
                            'v_out': v_out,
                            'v_lim': v_lim,
                            'i_range': i_range_select,
                            'i_limit': i_limit,
                            'sampling': sampling
                        })
            elif self.sensor_type.value == 'Diode':
                for i in range(8):
                    smu = f"SMU{(i//2)+1}"
                    ch = f"CH{(i%2)+1}"
                    with ui.row().style('margin-bottom: 4px; align-items: center;'):
                        enabled = ui.checkbox(value=False)
                        smu_label = ui.label(f'{smu}-{ch}').style('width: 100px; font-weight: bold;')
                        com_port = ui.select(options=self.available_ports, value=self.available_ports[0] if self.available_ports else None).style('width: 70px;')
                        sensor_name = ui.input(placeholder=f'Sensor {i+1}', value=f'Sensor {i+1}').style('width: 95px;')

                        v_out_start = ui.number(value=0.0, min=-10, max=10, step=0.1).style('width: 60px;')
                        v_out_stop = ui.number(value=2.0, min=-10, max=10, step=0.1).style('width: 60px;')
                        v_out_step = ui.number(value=0.5, min=0.00001, max=1, step=0.01).style('width: 60px;')

                        v_lim = ui.number(value=10.5, min=0, max=10.5, step=0.1).style('width: 60px;')

                        i_range_select = ui.select(options=list(current_ranges.keys()), value='200 mA').style('width: 90px;')

                        i_limit = ui.number(value=225, min=0, max=225, step=1).style('width: 80px;')

                        sampling = ui.select(options=sampling_rates, value='1024').style('width: 70px;')

                        self.sensor_config.append({
                            'enabled': enabled,
                            'name': sensor_name,
                            'smu': smu,
                            'channel': ch,
                            'com_port': com_port,
                            'v_out_start': v_out_start,
                            'v_out_stop': v_out_stop,
                            'v_out_step': v_out_step,
                            'v_lim': v_lim,
                            'i_range': i_range_select,
                            'i_limit': i_limit,
                            'sampling': sampling
                        })
    #Functions to update the preview plot 
    def update_preview_plot(self):
        stab_time = self.stab_time.value
        expo_time = self.expo_time.value
        rec_time = self.rec_time.value
        
        x_data = []
        y_data = []
        t = 0

        if self.test_type.value == 'Linear':
            start = self.lin_start.value
            stop = self.lin_stop.value
            step = self.lin_step.value
            t += stab_time
            x_data.append(t)   # Stabilization
            y_data.append(0)
            for ppm in range(int(start), int(stop + 1), int(step)):
                t += expo_time
                x_data.append(t)   # Exposure
                y_data.append(ppm)
                t += rec_time
                x_data.append(t)   # Step
                y_data.append(0)
               
        elif self.test_type.value == 'Pulse':
            pulse_ppm = self.pulse_ppm.value
            pulse_count = self.pulse_count.value
            t += stab_time
            x_data.append(t)   # Stabilization
            y_data.append(0)
            for _ in range(int(pulse_count)):
                t += expo_time
                x_data.append(t)   # Exposure
                y_data.append(pulse_ppm)
                t += rec_time
                x_data.append(t)   # Step
                y_data.append(0)
                
        elif self.test_type.value == 'Custom':
            try:
                ppm_values = [int(v.strip()) for v in self.custom_ppm_list.value.split(',') if v.strip()]
            except ValueError:
                ui.notify('Invalid input in Custom PPM list.', type='negative')
                return
            t += stab_time
            x_data.append(t)   # Stabilization
            y_data.append(0)
            for ppm in ppm_values:
                t += expo_time
                x_data.append(t)   # Exposure
                y_data.append(ppm)
                t += rec_time
                x_data.append(t)   # Step
                y_data.append(0)
                
        # Update echart
        self.preview_plot.options['xAxis']['type'] = 'value'
        self.preview_plot.options['xAxis']['name'] = 'Time (m)'
        self.preview_plot.options['xAxis']['axisLabel'] = {'formatter': '{value}'}
        self.preview_plot.options['yAxis']['name'] = 'ppm'
        self.preview_plot.options['series'] = [{
            'type': 'line',
            'step': 'start',
            'data': list(zip(x_data, y_data)),
            'name': 'PPM',
            'areaStyle': {}  
        }]
        self.preview_plot.update()
    
    def collect_config(self):
        config = {
            'carrier_gas_ao': self.carrier_gas_analogOut.value,
            'carrier_gas_initialPPM': self.carrier_gas_initialppm.value,
            'carrier_gas_maxFlow': self.carrier_gas_maxflow.value,
            'target_gas_ao': self.target_gas_analogOut.value,
            'target_gas_initialPPM': self.target_gas_initialppm.value,
            'target_gas_maxFlow': self.target_gas_maxflow.value,
            'interfering_gas_ao': self.interfering_gas_analogOut.value,
            'interfering_gas_initialPPM': self.interfering_gas_initialppm.value,
            'interfering_gas_maxFlow': self.interfering_gas_maxflow.value,
            'totalFlow' : self.totalflow.value,
            'test_type': self.test_type.value,
            'stab_time': self.stab_time.value,
            'expo_time': self.expo_time.value,
            'rec_time': self.rec_time.value,
            'sample_freq' : self.sample_freq.value,
            'sensor_type': self.sensor_type.value,
            'smu_setup': self.sensor_config,
        }
        if self.test_type.value == 'Linear':
            config.update({
                'lin_start': self.lin_start.value,
                'lin_stop': self.lin_stop.value,
                'lin_step': self.lin_step.value,
            })
        elif self.test_type.value == 'Pulse':
            config.update({
                'pulse_ppm': self.pulse_ppm.value,
                'pulse_count': self.pulse_count.value,
            })
        elif self.test_type.value == 'Custom':
            config.update({
                'custom_ppm_list': self.custom_ppm_list.value,
            })
        return config
    
    def update_results_layout(self):
        self.results_state = {}
        self.results_section.clear()

        if self.sensor_type.value == 'Resistor':
            sensor = 'Resistor'
            with self.results_section:
                with ui.grid(columns=4).style('gap: 20px;'):
                    sensor_setup = self.experiment_config['smu_setup']
                    for i, config in enumerate(sensor_setup):
                        if not config['enabled'].value:
                             continue
                        sensor_name = config['name'].value
                        with ui.card().style('width: 380px; margin: 1%;  display: inline-block; padding: 10px;'):
                            ui.label(f'{sensor_name}').style('font-weight: bold; font-size: 16px; margin-bottom: 5px;')
                            # Temperature and humidity
                            temp_label = ui.label('Temp: -- °C').style('font-size: 14px;')
                            rh_label = ui.label('Humidity: -- %RH').style('font-size: 14px;')

                            # Dual Y-axis plot (Resistance vs Time + PPM)
                            chart = ui.echart({
                                'tooltip': {'trigger': 'axis'},
                                'xAxis': {'type': 'value', 'name': 't (s)'},
                                'yAxis': [
                                    {'type': 'value', 'name': 'R(Ω)', 'position': 'left'},
                                    {'type': 'value', 'name': 'PPM', 'position': 'right'}
                                ],
                                'series': [
                                    {'name': 'R(Ω)', 'type': 'line', 'yAxisIndex': 0, 'data': []},
                                    {'name': 'PPM', 'type': 'line', 'yAxisIndex': 1, 'data': []}
                                ],
                                'legend': {'data': ['R(Ω)', 'PPM']}
                            }).style('width: 100%; height: 400px; margin-top: 5px;')

                            # CSV Export
                            ui.button('Export CSV', icon='download', on_click=lambda s=sensor_name: self.export_csv(s,sensor,0,0)).style('margin-top: 0px; width: 100%;')

                            # Save the widgets for real-time updates
                            self.results_state[sensor_name] = {
                                'temp_label': temp_label,
                                'rh_label': rh_label,
                                'chart': chart,
                                'data': [],  # Optional: store [t, R, PPM, T, RH] here for CSV
                                'smu_config' : config
                            }

        elif self.sensor_type.value == 'Transistor':
            sensor = 'Transistor'
            with self.results_section:
                with ui.grid(columns=4).style('gap: 20px;'):
                    sensor_setup = self.experiment_config['smu_setup']
                    for i, config in enumerate(sensor_setup):
                        if not config['enabled'].value:
                            continue
                        sensor_name = config['name'].value
                        with ui.card().style('width: 380px; margin: 1%; display: inline-block; padding: 10px;'):
                            ui.label(f'{sensor_name}').style('font-weight: bold; font-size: 16px; margin-bottom: 5px;')
                            temp_label = ui.label('Temp: -- °C').style('font-size: 14px;')
                            rh_label   = ui.label('Humidity: -- %RH').style('font-size: 14px;')
                            vgs_start = config['v_gate_start'].value
                            vgs_stop = config['v_gate_stop'].value
                            if vgs_start != vgs_stop:
                            #Id vs Vgs chart (for Vgs sweep)
                                chart = ui.echart({
                                    'tooltip': {'trigger': 'axis'},
                                    'xAxis':   {'type': 'value', 'name': 'VG (V)'},
                                    'yAxis':   {'type': 'value', 'name': 'ID (A)'},
                                    'series':  [{'name': 'ID–VG', 'type': 'line', 'data': []}],
                                    'legend':  {'data': ['ID–VG']}
                                }).style('width: 100%; height: 400px; margin-top: 5px;')
                                
                            else:
                            #Is vs Time chart (for static Vgs)
                                chart = ui.echart({
                                    'tooltip': {'trigger': 'axis'},
                                    'xAxis': {'type': 'value', 'name': 't (s)'},
                                    'yAxis': [
                                        {'type': 'value', 'name': 'I(A)', 'position': 'left'},
                                        {'type': 'value', 'name': 'PPM', 'position': 'right'}
                                    ],
                                    'series': [
                                        {'name': 'I(A)', 'type': 'line', 'yAxisIndex': 0, 'data': []},
                                        {'name': 'PPM', 'type': 'line', 'yAxisIndex': 1, 'data': []}
                                    ],
                                    'legend': {'data': ['I(A)', 'PPM']}
                                }).style('width: 100%; height: 400px; margin-top: 5px;')

                            ui.button( 'Export CSV', icon='download', on_click=lambda s=sensor_name, sn=sensor, vs=vgs_start, ve=vgs_stop: self.export_csv(s, sn, vs, ve) ).style('margin-top: 0px; width: 100%;')
                            self.results_state[sensor_name] = {
                                'temp_label': temp_label,
                                'rh_label':   rh_label,
                                'chart':      chart,
                                'data':       [],
                                'smu_config' : config,
                                'counter' : 0
                            }
        elif self.sensor_type.value == 'Diode':
            sensor = 'Diode'
            with self.results_section:
                with ui.grid(columns=4).style('gap: 20px;'):
                    sensor_setup = self.experiment_config['smu_setup']
                    for i, config in enumerate(sensor_setup):
                        if not config['enabled'].value:
                             continue
                        sensor_name = config['name'].value
                        with ui.card().style('width: 380px; margin: 1%;  display: inline-block; padding: 10px;'):
                            ui.label(f'{sensor_name}').style('font-weight: bold; font-size: 16px; margin-bottom: 5px;')
                            # Temperature and humidity
                            temp_label = ui.label('Temp: -- °C').style('font-size: 14px;')
                            rh_label = ui.label('Humidity: -- %RH').style('font-size: 14px;')
                            vout_start = config['v_out_start'].value
                            vout_stop = config['v_out_stop'].value
                            if vout_start != vout_stop:
                            #I vs V chart (for V sweep)
                                chart = ui.echart({
                                    'tooltip': {'trigger': 'axis'},
                                    'xAxis':   {'type': 'value', 'name': 'V (V)'},
                                    'yAxis':   {'type': 'value', 'name': 'I (A)'},
                                    'series':  [{'name': 'I–V', 'type': 'line', 'data': []}],
                                    'legend':  {'data': ['I–V']}
                                }).style('width: 100%; height: 400px; margin-top: 5px;')
                            else:
                                #I vs Time chart (for static V)
                                # Dual Y-axis plot (Resistance vs Time + PPM)
                                chart = ui.echart({
                                    'tooltip': {'trigger': 'axis'},
                                    'xAxis': {'type': 'value', 'name': 't (s)'},
                                    'yAxis': [
                                        {'type': 'value', 'name': 'I(A)', 'position': 'left'},
                                        {'type': 'value', 'name': 'PPM', 'position': 'right'}
                                    ],
                                    'series': [
                                        {'name': 'I(A)', 'type': 'line', 'yAxisIndex': 0, 'data': []},
                                        {'name': 'PPM', 'type': 'line', 'yAxisIndex': 1, 'data': []}
                                    ],
                                    'legend': {'data': ['I(A)', 'PPM']}
                                }).style('width: 100%; height: 400px; margin-top: 5px;')

                            # CSV Export
                            ui.button( 'Export CSV', icon='download', on_click=lambda s=sensor_name, sn=sensor, vs=vout_start, ve=vout_stop: self.export_csv(s, sn, vs, ve) ).style('margin-top: 0px; width: 100%;')

                            # Save the widgets for real-time updates
                            self.results_state[sensor_name] = {
                                'temp_label': temp_label,
                                'rh_label': rh_label,
                                'chart': chart,
                                'data': [], 
                                'smu_config' : config,
                                'counter' : 0
                            }

    def export_csv(self, sensor_name, sensor_type,v_start,v_stop):
        if sensor_name not in self.results_state:
            ui.notify(f"No data found for sensor: {sensor_name}", type='warning')
            return

        data = self.results_state[sensor_name]['data']
        if not data:
            ui.notify(f"No data to export for sensor: {sensor_name}", type='warning')
            return

        filename = f'{sensor_name.replace(" ", "_")}_results.csv'
        filepath = Path('results') / filename
        filepath.parent.mkdir(exist_ok=True)

        # Write CSV
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if sensor_type == 'Resistor':
                writer.writerow(['Time (s)', 'Resistance (Ω)', 'PPM', 'Temperature (°C)', 'Humidity (%RH)'])
            elif sensor_type =='Transistor':
                if v_start != v_stop:
                    writer.writerow(['Vgs (V)', 'Id (A)', 'PPM', 'Temperature (°C)', 'Humidity (%RH)'])
                else:
                    writer.writerow(['Time (s)', 'Current (A)', 'PPM', 'Temperature (°C)', 'Humidity (%RH)'])
            elif sensor_type =='Diode':
                if v_start != v_stop:
                    writer.writerow(['V (V)', 'I (A)', 'PPM', 'Temperature (°C)', 'Humidity (%RH)'])
                else:
                    writer.writerow(['Time (s)', 'Current (A)', 'PPM', 'Temperature (°C)', 'Humidity (%RH)'])
            writer.writerows(data)

        ui.notify(f'Data exported: {filepath}', type='positive')

    async def update_sensors(self, config, step, phase, ppm):
        sensor_type = config['sensor_type']
        for sensor_name, widgets in self.results_state.items():
            smu_config = widgets['smu_config']
            chart = widgets['chart']
            if sensor_type == 'Resistor':
                data = await get_sensor_data(sensor_type, ppm, smu_config, self.labjack)
                # Update environment labels
                widgets['temp_label'].set_text(f"Temp: {data['temp']} °C")
                widgets['rh_label'].set_text(f"Humidity: {data['rh']} %RH")

                resistance = data['resistance']
                chart.options['series'][0]['data'].append([step/config['sample_freq'], resistance])
                chart.options['series'][1]['data'].append([step/config['sample_freq'], ppm])
                chart.update()
                widgets['data'].append([step, resistance, ppm, data['temp'], data['rh']])

            elif sensor_type == 'Transistor':
                vgs_start = smu_config['v_gate_start'].value
                vgs_stop = smu_config['v_gate_stop'].value
                #Choose between (Vgs vs Id) and (Id vs time)
                if vgs_start != vgs_stop:
                    widgets['counter'] += 1
                    if widgets['counter'] > (config['sample_freq'] * 2): #It just get the sensors data after 2 seconds
                        data = await get_sensor_data(sensor_type, ppm, smu_config)
                        print(f'Data return chech: {data}')
                        # Update environment labels
                        widgets['temp_label'].set_text(f"Temp: {data['temp']} °C")
                        widgets['rh_label'].set_text(f"Humidity: {data['rh']} %RH")
                    # pull out gate‑voltage and drain‑current
                        vgs    = data['vgs']
                        id_val = data['id']
                        chart.options['series'][0]['data'].append(None)
                        chart.options['series'][0]['data'].extend([[vg, id_] for vg, id_ in zip(vgs, id_val)])
                        chart.update()
                    # also save to your CSV buffer
                        widgets['data'].append([vgs, id_val, ppm, data['temp'], data['rh']])
                        widgets['counter'] = 0
                else:
                    #Id vs Time (for a fixed Vg and Vd)
                    data = await get_sensor_data(sensor_type, ppm, smu_config)
                    # Update environment labels
                    widgets['temp_label'].set_text(f"Temp: {data['temp']} °C")
                    widgets['rh_label'].set_text(f"Humidity: {data['rh']} %RH")
                    
                    id_val = data['current'][0] if isinstance(data['current'], list) else data['current']
                    chart.options['series'][0]['data'].append([step / config['sample_freq'], id_val])
                    chart.options['series'][1]['data'].append([step / config['sample_freq'], ppm])
                    chart.update()

                    widgets['data'].append([step, id_val, ppm, data['temp'], data['rh']])

            elif sensor_type == "Diode" :
                vout_start = smu_config['v_out_start'].value
                vout_stop = smu_config['v_out_stop'].value
                #Choose between (V vs I) and (I vs time)
                if vout_start != vout_stop:
                    widgets['counter'] += 1
                    if widgets['counter'] > (config['sample_freq'] * 2): #It just get the sensors data after 2 seconds
                        data = await get_sensor_data(sensor_type, ppm, smu_config)
                        # Update environment labels
                        widgets['temp_label'].set_text(f"Temp: {data['temp']} °C")
                        widgets['rh_label'].set_text(f"Humidity: {data['rh']} %RH")
                    # pull out voltage and current
                        vout    = data['vout']
                        i_val = data['i_val']
                        chart.options['series'][0]['data'].append(None)
                        chart.options['series'][0]['data'].extend([[v, i_] for v, i_ in zip(vout, i_val)])
                        chart.update()
                    # also save to your CSV buffer
                        widgets['data'].append([vout, i_val, ppm, data['temp'], data['rh']])
                        widgets['counter'] = 0
                else:
                    #I vs Time (for a fixed Vout)
                    data = await get_sensor_data(sensor_type, ppm, smu_config)
                    # Update environment labels
                    widgets['temp_label'].set_text(f"Temp: {data['temp']} °C")
                    widgets['rh_label'].set_text(f"Humidity: {data['rh']} %RH")
                    
                    i_val = data['current'][0] if isinstance(data['current'], list) else data['current']
                    chart.options['series'][0]['data'].append([step / config['sample_freq'], i_val])
                    chart.options['series'][1]['data'].append([step / config['sample_freq'], ppm])
                    chart.update()

                    widgets['data'].append([step, i_val, ppm, data['temp'], data['rh']])


    # Runs the experiment simulation
    async def run_experiment(self):
        self.start_btn.disable()
        self.stop_btn.enable()

        config = self.experiment_config  # User parameters

        def frange(start, stop, step):
            while start <= stop:
                yield round(start, 4)
                start += step

        ###### Find the sequence pattern for the gas exposure ######
        test_type = config['test_type']
        if test_type == 'Linear':
            start = config['lin_start']
            stop = config['lin_stop']
            step = config['lin_step']
            sequence = [round(v, 2) for v in frange(start, stop, step)]
        elif test_type == 'Pulse':
            sequence = [config['pulse_ppm']] * config['pulse_count']
        elif test_type == 'Custom':
            sequence = [float(ppm.strip()) for ppm in config['custom_ppm_list'].split(',') if ppm.strip()]

        sample_freq = config['sample_freq']
        sample_period = 1/sample_freq
        sim_unit = 1 # 60 for minutes, 1 for seconds
        # Timing logic convert minutes to steps
        stab_steps = int(config['stab_time'] * sim_unit * sample_freq) 
        expo_steps = int(config['expo_time'] * sim_unit * sample_freq)
        rec_steps  = int(config['rec_time']  * sim_unit * sample_freq)

        self.running = True
        ################## Stabilization ####################
        self.status_label.set_text("Status: Stabilization time...")
        flows = calculate_gas_flows(0, config)
        target_flow_setpoint = flows['target_flow'] #This returns 0 sccm for the target gas
        carrier_flow_setpoint = flows['carrier_flow'] #This returns the total flow for the carrier gas
        # Convert to initial voltages
        v_target = flow_to_voltage(target_flow_setpoint, config['target_gas_maxFlow'])
        v_carrier = flow_to_voltage(carrier_flow_setpoint, config['carrier_gas_maxFlow'])
        # Set the volatge output for each MFC
        set_analog_output(self.labjack, config['target_gas_ao'], v_target)
        set_analog_output(self.labjack, config['carrier_gas_ao'], v_carrier)

        # PID state variables for target gas
        integral_target = 0.0
        prev_error_target = 0.0

        # PID state variables for carrier gas
        integral_carrier = 0.0
        prev_error_carrier = 0.0

        # PID gains
        Kp_target, Ki_target, Kd_target = 0.8, 0.1, 0.05
        Kp_carrier, Ki_carrier, Kd_carrier = 0.8, 0.1, 0.05

        for step in range(stab_steps):
            if not self.running:
                break
            # Read feedback voltages for both gases
            feedback_voltage_target = get_analog_feedback(self.labjack, config['target_gas_ao'])
            feedback_voltage_carrier = get_analog_feedback(self.labjack, config['carrier_gas_ao'])

            # PID update for target gas
            pid_voltage_target, integral_target, prev_error_target = pid_update(
                target_flow_setpoint, feedback_voltage_target,
                integral_target, prev_error_target,
                Kp_target, Ki_target, Kd_target,
                sample_period, config['target_gas_maxFlow']
            )

            # PID update for carrier gas
            pid_voltage_carrier, integral_carrier, prev_error_carrier = pid_update(
                carrier_flow_setpoint, feedback_voltage_carrier,
                integral_carrier, prev_error_carrier,
                Kp_carrier, Ki_carrier, Kd_carrier,
                sample_period, config['carrier_gas_maxFlow']
            )

            # Set outputs using PID voltages
            set_analog_output(self.labjack, config['target_gas_ao'], pid_voltage_target)
            set_analog_output(self.labjack, config['carrier_gas_ao'], pid_voltage_carrier)

            await self.update_sensors(config, step, 'stabilization', 0)
            self.progress_bar.value = step
            await asyncio.sleep(sample_period)

        total_phase = len(sequence)
        current_step = stab_steps

        for i, ppm in enumerate(sequence):
            if not self.running:
                break
            ################### Exposure ##################
            self.status_label.set_text(f"Status: Exposure ({i+1}/{total_phase}) - {ppm} ppm")
            flows = calculate_gas_flows(ppm, config)
            target_flow_setpoint = flows['target_flow']
            carrier_flow_setpoint = flows['carrier_flow']
            # Convert to initial voltages
            v_target = flow_to_voltage(target_flow_setpoint, config['target_gas_maxFlow'])
            v_carrier = flow_to_voltage(carrier_flow_setpoint, config['carrier_gas_maxFlow'])
            #Apply voltages to the MFC
            set_analog_output(self.labjack, config['target_gas_ao'], v_target)
            set_analog_output(self.labjack, config['carrier_gas_ao'], v_carrier)

            # PID state variables for target gas
            integral_target = 0.0
            prev_error_target = 0.0

            # PID state variables for carrier gas
            integral_carrier = 0.0
            prev_error_carrier = 0.0

            # PID gains
            Kp_target, Ki_target, Kd_target = 0.8, 0.1, 0.05
            Kp_carrier, Ki_carrier, Kd_carrier = 0.8, 0.1, 0.05

            for s in range(expo_steps):
                if not self.running:
                    break

                # Read feedback voltages for both gases
                feedback_voltage_target = get_analog_feedback(self.labjack, config['target_gas_ao'])
                feedback_voltage_carrier = get_analog_feedback(self.labjack, config['carrier_gas_ao'])

                # PID update for target gas
                pid_voltage_target, integral_target, prev_error_target = pid_update(
                    target_flow_setpoint, feedback_voltage_target,
                    integral_target, prev_error_target,
                    Kp_target, Ki_target, Kd_target,
                    sample_period, config['target_gas_maxFlow']
                )

                # PID update for carrier gas
                pid_voltage_carrier, integral_carrier, prev_error_carrier = pid_update(
                    carrier_flow_setpoint, feedback_voltage_carrier,
                    integral_carrier, prev_error_carrier,
                    Kp_carrier, Ki_carrier, Kd_carrier,
                    sample_period, config['carrier_gas_maxFlow']
                )

                # Set outputs using PID voltages
                set_analog_output(self.labjack, config['target_gas_ao'], pid_voltage_target)
                set_analog_output(self.labjack, config['carrier_gas_ao'], pid_voltage_carrier)

                await self.update_sensors(config, current_step, 'exposure', ppm)
                self.progress_bar.value = current_step
                current_step += 1
                await asyncio.sleep(sample_period)

            ################# Recovery ##################
            self.status_label.set_text(f"Status: Recovery ({i+1}/{total_phase})")
            flows = calculate_gas_flows(0, config)
            target_flow_setpoint = flows['target_flow'] #This returns 0 sccm for the target gas
            carrier_flow_setpoint = flows['carrier_flow'] #This returns the total flow for the carrier gas
            # Convert to initial voltages
            v_target = flow_to_voltage(target_flow_setpoint, config['target_gas_maxFlow'])
            v_carrier = flow_to_voltage(carrier_flow_setpoint, config['carrier_gas_maxFlow'])
            set_analog_output(self.labjack, config['target_gas_ao'], v_target)
            set_analog_output(self.labjack, config['carrier_gas_ao'], v_carrier)

            # PID state variables for target gas
            integral_target = 0.0
            prev_error_target = 0.0

            # PID state variables for carrier gas
            integral_carrier = 0.0
            prev_error_carrier = 0.0

            # PID gains
            Kp_target, Ki_target, Kd_target = 0.8, 0.1, 0.05
            Kp_carrier, Ki_carrier, Kd_carrier = 0.8, 0.1, 0.05

            for s in range(rec_steps):
                if not self.running:
                    break

                # Read feedback voltages for both gases
                feedback_voltage_target = get_analog_feedback(self.labjack, config['target_gas_ao'])
                feedback_voltage_carrier = get_analog_feedback(self.labjack, config['carrier_gas_ao'])

                # PID update for target gas
                pid_voltage_target, integral_target, prev_error_target = pid_update(
                    target_flow_setpoint, feedback_voltage_target,
                    integral_target, prev_error_target,
                    Kp_target, Ki_target, Kd_target,
                    sample_period, config['target_gas_maxFlow']
                )

                # PID update for carrier gas
                pid_voltage_carrier, integral_carrier, prev_error_carrier = pid_update(
                    carrier_flow_setpoint, feedback_voltage_carrier,
                    integral_carrier, prev_error_carrier,
                    Kp_carrier, Ki_carrier, Kd_carrier,
                    sample_period, config['carrier_gas_maxFlow']
                )

                # Set outputs using PID voltages
                set_analog_output(self.labjack, config['target_gas_ao'], pid_voltage_target)
                set_analog_output(self.labjack, config['carrier_gas_ao'], pid_voltage_carrier)

                await self.update_sensors(config, current_step, 'recovery', 0)
                self.progress_bar.value = current_step
                current_step += 1
                await asyncio.sleep(sample_period)
        
        self.running = False
        self.status_label.set_text("Status: Finished")
        self.start_btn.enable()
        self.stop_btn.disable()

    # Starts the experiment
    def start_experiment(self):
        if self.running:
            return
        
        self.error_list.clear()
        error_messages = []
        #Call the function to collect all the user parameters
        self.experiment_config = self.collect_config()

        ###### Error Checking ########
        # Collect AO assignments
        ao_assignments = {
            'Carrier Gas': self.carrier_gas_analogOut.value,
            'Target Gas': self.target_gas_analogOut.value,
            # 'Interfering Gas': self.interfering_gas_analogOut.value
        }
        # Check if any AO is 'None'
        if 'None' in ao_assignments.values():
            error_messages.append('All gases must be assigned to an AO (AO0, AO1, AO2).')
            self.tabs.set_value('Environment Setup')
        # Check for duplicates
        assigned_aos = list(ao_assignments.values())
        if len(assigned_aos) != len(set(assigned_aos)):
            error_messages.append('Each gas must be assigned to a unique AO.')
            self.tabs.set_value('Environment Setup')

        # Check if the target gas cylinder concentration is not zero
        if self.target_gas_initialppm.value == 0:
            error_messages.append('Target gas cylinder concentration (PPM) cannot be zero.')
            self.tabs.set_value('Environment Setup')
        
        # Max flows must be non-zero
        if self.carrier_gas_maxflow.value == 0:
            error_messages.append('Carrier gas max flow must be greater than zero.')
            self.tabs.set_value('Environment Setup')
        if self.target_gas_maxflow.value == 0:
            error_messages.append('Target gas max flow must be greater than zero.')
            self.tabs.set_value('Environment Setup')

        # Total flow check
        if self.totalflow.value > (self.carrier_gas_maxflow.value + self.target_gas_maxflow.value):
            error_messages.append('Total flow cannot be greater than the sum of carrier and target gas max flows.')
            self.tabs.set_value('Environment Setup')

        # Maximum PPM in selected test must not exceed the cylinder concentration
        if self.test_type.value == 'Linear':
            if self.lin_stop.value > self.target_gas_initialppm.value:
                error_messages.append('Stop PPM in linear test cannot exceed the target gas cylinder concentration.')
                self.tabs.set_value('Test Setup')
        elif self.test_type.value == 'Pulse':
            if self.pulse_ppm.value > self.target_gas_initialppm.value:
                error_messages.append('Pulse PPM cannot exceed the target gas cylinder concentration.')
                self.tabs.set_value('Test Setup')
        elif self.test_type.value == 'Custom':
            ppm_values = [float(ppm.strip()) for ppm in self.experiment_config['custom_ppm_list'].split(',') if ppm.strip()]
            if any(ppm > self.target_gas_initialppm.value for ppm in ppm_values):
                error_messages.append('One or more custom PPM values exceed the target gas cylinder concentration.')
                self.tabs.set_value('Test Setup')

        for i,sensor_config in enumerate(self.experiment_config['smu_setup']):
            if not sensor_config['enabled'].value:
                continue
            sensor_name = sensor_config['name'].value
            if self.experiment_config['sensor_type'] == 'Transistor':
                vgs_start = sensor_config['v_gate_start'].value
                vgs_stop = sensor_config['v_gate_stop'].value
                vstep = sensor_config['v_gate_step'].value
                osr_value = int(sensor_config['sampling'].value)
                if vgs_start != vgs_stop:
                    if (128 <= osr_value <= 1024 and vstep < 0.0001) or (2048 <= osr_value <= 32768 and vstep < 0.00001) or ((osr_value < 128 or osr_value > 32768) and vstep < 0.0001):
                        min_allowed = 0.00001 if 2048 <= osr_value <= 32768 else 0.0001
                        error_messages.append(
                            f"[{sensor_name}] Step voltage {vstep} V is too small for SR {osr_value}. "
                            f"Minimum allowed: {min_allowed} V"
                        )
                        self.tabs.set_value('SMU Setup')
                    if abs(vgs_stop - vgs_start) < vstep:
                        error_messages.append(
                            f"[{sensor_name}] Voltage step is too large for the selected range (start: {vgs_start} V, stop: {vgs_stop} V, step: {vstep} V)."
                        )
                        self.tabs.set_value('SMU Setup')

        # Display errors
        if error_messages:
            for msg in error_messages:
                with self.error_list:
                    with ui.item():
                        ui.icon('error').classes('text-red-500')
                        ui.label(msg)
            ui.notify('Some parameters are incorrect. See error checklist.', type='negative')
            return

        self.tabs.set_value('Results')
        # If no errors, clear previous messages
        self.status_label.set_text('')
        #Call the function to debug the parameters, it can be commented later if debbuging is not necessary
        self.print_user_parameters()
        #Call the function to update the layout of the results tab
        self.update_results_layout()
        

        # Passed validation: run experiment
        asyncio.create_task(self.run_experiment())

    # Stops the experiment
    def stop_experiment(self):
        self.running = False
        self.status_label.set_text('Status: Stopped by user')
        self.start_btn.enable()
        self.stop_btn.disable()
    
    #Debugging of the user input parameters in terminal
    def print_user_parameters(self):
        print('\n--- USER PARAMETERS ---')
        print(f'Carrier Gas:')
        print(f'  AO: {self.carrier_gas_analogOut.value}')
        print(f'  Initial ppm: {self.carrier_gas_initialppm.value}')
        print(f'  Max Flow: {self.carrier_gas_maxflow.value}')
        print(f'Target Gas:')
        print(f'  AO: {self.target_gas_analogOut.value}')
        print(f'  Initial ppm: {self.target_gas_initialppm.value}')
        print(f'  Max Flow: {self.target_gas_maxflow.value}')
        print(f'Interfering Gas:')
        print(f'  AO: {self.interfering_gas_analogOut.value}')
        print(f'  Initial ppm: {self.interfering_gas_initialppm.value}')
        print(f'  Max Flow: {self.interfering_gas_maxflow.value}')

        print(f'\nTiming Setup:')
        print(f'  Stabilization Time: {self.stab_time.value} m')
        print(f'  Exposure Time: {self.expo_time.value} m')
        print(f'  Recovery Time: {self.rec_time.value} m')

        print(f'\nSensor Type: {self.sensor_type.value}')
        
        print(f'\nTest Type: {self.test_type.value}')
        if self.test_type.value == 'Linear':
            print(f'  Start ppm: {self.lin_start.value}')
            print(f'  Stop ppm: {self.lin_stop.value}')
            print(f'  Step ppm: {self.lin_step.value}')
        elif self.test_type.value == 'Pulse':
            print(f'  Pulse ppm: {self.pulse_ppm.value}')
            print(f'  Pulse Count: {self.pulse_count.value}')
        elif self.test_type.value == 'Custom':
            print(f'  Custom ppm List: {self.custom_ppm_list.value}')

        print(f'\nSMU Setup:')
        current_ranges_map = {
            'Autorange': 1.0,
            '200 mA': 0.2,
            '20 mA': 0.02,
            '2 mA': 0.002,
            '200 µA': 0.0002,
            '20 µA': 0.00002
        }

        unit_scaling = {
            '200 mA': ('mA', 1e-3),
            '20 mA': ('mA', 1e-3),
            '2 mA': ('mA', 1e-3),
            '200 µA': ('µA', 1e-6),
            '20 µA': ('µA', 1e-6),
            'Autorange': ('Auto', 1)
        }

        for i, config in enumerate(self.sensor_config, start=1):
            if config['enabled'].value:
                smu_ch = f"{config['smu']}-{config['channel']}"
                name = config['name'].value
                i_range_label = config['i_range'].value
                i_lim_display = config['i_limit'].value
                sampling = config['sampling'].value
                com_port = config['com_port'].value
                print(f'  Sensor {i}: {name}')
                print(f'    SMU-CH: {smu_ch}')
                if 'v_drain' in config:
                    v_drain = config['v_drain'].value
                    v_gate_start = config['v_gate_start'].value
                    v_gate_stop = config['v_gate_stop'].value
                    v_gate_step = config['v_gate_step'].value
                    print(f'    Drain Voltage: {v_drain} V')
                    print(f'    Gate Sweep: Start={v_gate_start} V, Stop={v_gate_stop} V, Step={v_gate_step} V')
                elif 'v_out_stop' in config:
                    v_out_start = config['v_out_start'].value
                    v_out_stop = config['v_out_stop'].value
                    v_out_step = config['v_out_step'].value
                    print(f'    Voltage Sweep: Start={v_out_start} V, Stop={v_out_stop} V, Step={v_out_step} V')
                else:
                    v_out = config['v_out'].value
                    v_lim = config['v_lim'].value
                    print(f'    V Out: {v_out} V')
                    print(f'    V Lim: {v_lim} V')
                if i_range_label == 'Autorange':
                    print(f'    I Range: Autorange (handled automatically by SMU)')
                    print(f'    I Lim: {i_lim_amp} A (user input: {i_lim_display} mA)')
                else:
                    i_range_amp = current_ranges_map[i_range_label]
                    _, scale = unit_scaling[i_range_label]
                    i_lim_amp = i_lim_display * scale
                    print(f'    I Range: {i_range_amp} A (user input: {i_range_label})')
                    print(f'    I Lim: {i_lim_amp} A (user input: {i_lim_display} mA)')

                print(f'    Sampling Rate: {sampling}')
                print(f'    COM Port: {com_port}')

# Runs the app
if __name__ in {"__main__", "__mp_main__"}:
    print("Opening LabJack U6...")
    com_ports = serial.tools.list_ports.comports()
    try:
        labjack = u6.U6()
        print(f"Connected to LabJack U6 with serial #{labjack.serialNumber}")
    except Exception as e:
        print(f"LabJack connection failed: {e}")
        labjack = None
    gas_app = GasSensorApp(labjack,com_ports)
    ui.run(port=8090, reload=False)

