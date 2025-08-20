# from nicegui import ui
# import asyncio
# import matplotlib
# import random
# import csv
# from pathlib import Path


# # Main GUI class
# class GasSensorApp:
#     def __init__(self):
#         self.running = False
#         dark = ui.dark_mode()
#         ui.switch('Dark mode').bind_value(dark)
#         ui.label('Gas Sensor Characterization Platform').style('font-size: 22px; font-weight: bold; margin-bottom: 0px;').classes('text-center')
#         with ui.tabs() as tabs:
#             setupTab = ui.tab('Environment Setup')
#             testTab = ui.tab('Test Setup')
#             smuTab = ui.tab('Gas Sensors Setup')
#             resultsTab = ui.tab('Results')
#         #Setup Tab
#         with ui.tab_panels(tabs, value=setupTab):
#             with ui.tab_panel(setupTab):
#                 # Layout: main row containing all columns
#                 with ui.row():
#                     # Column 1
#                     with ui.column():
#                         ui.label('MFC Setup').style('font-size: 18px; font-weight: bold; margin-top: 0px; margin-left: 0px;')
#                         with ui.card():
#                             with ui.row().style('justify-content: space-between; width: 1350px;'):
#                                 ui.label('Gas Name').style('margin-left: 320px; width: 140px; font-weight: bold;')
#                                 ui.label('Analog Output').style('margin-left: -20px; width: 140px; font-weight: bold; ')
#                                 ui.label('Full Scale Flow (sccm)').style('margin-left: -20px; width: 160px; font-weight: bold; ')
#                                 ui.label('Cylinder Concentration (ppm)').style('width: 200px; font-weight: bold; margin-left: 0px')

#                             for mfc_label in ['Carrier Gas', 'Target Gas', 'Interfering Gas']:
#                                 with ui.card().style('margin-top: -10px; margin-bottom: 0px; width: 1380px; font-size:15px;'):  # Wider card for table layout
#                                 # Build one row like a table
#                                     with ui.row().classes('items-center').style('gap: 170px;'):
                                        
#                                         # Column 1: Gas Name Label
#                                         ui.label(mfc_label).style('width: 150px; font-weight: bold;')
#                                         # Column 2: Gas Dropdown (menu for gas)
#                                         setattr(
#                                             self,
#                                             f'{mfc_label.lower().replace(" ", "_")}_gasType',
#                                             ui.select(
#                                                 options=['Air', 'N2', 'CO2', 'H2',],
#                                                 value='Air',
#                                             ).style('width: 100px;')
#                                         )
#                                         # Column 3: Analog Output Dropdown
#                                         setattr(
#                                             self,
#                                             f'{mfc_label.lower().replace(" ", "_")}_analogOut',
#                                             ui.select(
#                                                 options=['AO0', 'AO1', 'AO2', 'None'],
#                                                 value='None',
#                                             ).style('width: 100px;')
#                                         )
#                                         # Column 4: Full Scale Flow (sccm)
#                                         setattr(
#                                             self,
#                                             f'{mfc_label.lower().replace(" ", "_")}_maxflow',
#                                             ui.number(
#                                                 value=0, min=0, max=10000, step=1
#                                             ).style('width: 130px;')
#                                         )
#                                         # Column 5: Cylinder Concentration (ppm)
#                                         setattr(
#                                             self,
#                                             f'{mfc_label.lower().replace(" ", "_")}_initialppm',
#                                             ui.number(
#                                                 value=0, min=0, max=10000, step=1
#                                             ).style('width: 160px;')
#                                         )
                                        
#                         for mfc_label in ['Total Flow Rate (sccm)']:
#                                 with ui.card().style('margin-top: 20px; margin-left:10px; margin-bottom: 0px; width: 1380px; font-size:15px;'):  # Wider card for table layout
#                                 # Build one row like a table
#                                     with ui.row().classes('items-center').style('gap: 170px;'):
                                        
#                                         # Column 1: Total Flow Rate Label
#                                         ui.label(mfc_label).style('width: 150px; font-weight: bold;')
#                                         # Total Flow Rate
#                                         setattr(
#                                             self,
#                                             f'{mfc_label.lower().replace(" ", "_")}_maxflow',
#                                             ui.number(
#                                                 value=0, min=0, max=10000, step=1
#                                             ).style('width: 130px;')
#                                         )

#                         ui.label('Humidity Control').style('font-size: 18px; font-weight: bold; margin-top: 0px;')
#                         with ui.card().style('margin-bottom: 0px; width: 380px;'):
#                             with ui.row():
#                                 ui.label('Humidity Set Point (%RH)').style('width: 160px; font-size:15px; font-weight: bold; margin-top:10px;')
#                                 self.humidity_set_point = ui.number(value=50, min=0, max=100, step=1).style('width: 100px;')
#             with ui.tab_panel(testTab):
#                 with ui.row():
#                     #Column 2
#                     with ui.column():
#                         # Section: timing parameters for stabilization and recovery
#                         ui.label('Timing Setup').style('font-size: 18px; font-weight: bold; margin-top: 10px;')
#                         with ui.card().style('margin-bottom: 10px; width: 350px;'):
#                             with ui.row():
#                                 ui.label('Stabilization Time (m)').style('width: 150px;')
#                                 self.stab_time = ui.number(value=5, min=0, max=300, step=1).style('width: 100px;') # Stabilization time
#                             with ui.row():
#                                 ui.label('Exposure Time (m)').style('width: 150px;')
#                                 self.expo_time = ui.number(value=10, min=0, max=300, step=1).style('width: 100px;') # Exposure time
#                             with ui.row():
#                                 ui.label('Recovery Time (m)').style('width: 150px;')
#                                 self.rec_time = ui.number(value=5, min=0, max=300, step=1).style('width: 100px;') # Recovery time

                                
#                     with ui.column():
#                         #Section: test type
#                         ui.label('Test Type and Parameters').style('font-size: 18px; font-weight: bold; margin-top: 10px;')
#                         with ui.card().style('margin-bottom: 10px; width: 350px;'):
#                             self.test_type = ui.radio(['Linear', 'Pulse', 'Custom'], value='Linear') # Test selection
#                             self.cond_params = ui.column() # Parameters update 
#                             test_types = ['Linear', 'Pulse', 'Custom']
#                             self.test_type.on('update:model-value', lambda e: self.update_test_type_params(test_types[e.args]))
#                             self.update_test_type_params(self.test_type.value)
#                     # Column 4: Test Preview Plot and simulated real-time outputs
#                     with ui.column():
#                         ui.label('Test Preview Plot').style('font-size: 18px; font-weight: bold; margin-top: 10px;')
#                         with ui.card().style('margin-bottom: 10px; width: 650px; height: 500px;'):
#                             ui.button('Show Preview', on_click=self.update_preview_plot).style('margin-top: 10px;')
#                             self.preview_plot = ui.echart({
#                                 'xAxis': {
#                                     'type': 'value',
#                                     'name': 'Time (m)',
#                                     'axisLabel': {'formatter': '{value}'}
#                                 },
#                                 'yAxis': {'type': 'value', 'name': 'ppm'},
#                                 'series': [{
#                                     'type': 'line',
#                                     'step': 'start',
#                                     'data': [],
#                                     'name': 'PPM',
#                                     'areaStyle': {}  
#                                 }],
#                                 'tooltip': {'trigger': 'axis'}
#                             }).style('width: 600px; height: 500px;')

#             with ui.tab_panel(smuTab):
#                 with ui.row():
#                     with ui.column():                        
#                         #Section: Sensor type
#                         ui.label('Gas Sensor Type').style('font-size: 18px; font-weight: bold; margin-top: 0px;')
#                         with ui.card().style('margin-bottom: 10px; width: 350px;'):
#                             self.sensor_type = ui.radio(['Resistor', 'Transistor', 'Diode'], value='Resistor') # Sensor selection
                       
#                         # Start and stop buttons
#                         with ui.row().style('margin-top: 30px; justify-content: center;'):
#                             #self.start_btn = ui.button('Start', on_click=self.start_experiment)
#                             def handle_start_click():
#                                 self.start_experiment()
#                                 tabs.set_value('Results')

#                             self.start_btn = ui.button('Start', on_click=handle_start_click)
#                             self.start_btn.style('width: 120px; margin-right: 20px;')
#                             self.stop_btn = ui.button('Stop', on_click=self.stop_experiment)
#                             self.stop_btn.style('width: 120px;')
#                             self.stop_btn.disable()

#                         self.status_label = ui.label('Status: Idle').style('margin-top: 20px;')
#                         with ui.card().style('width: 400px; height: 200px;'):
#                             ui.label('Outputs').style('font-size: 18px; font-weight: bold; margin-bottom: 15px;').classes('text-center')
#                             # Progress bar
#                             ui.label('Experiment Progress').style('font-weight: bold; margin-top: 20px;')
#                             self.progress_bar = ui.linear_progress()
#                     with ui.column():
#                         # Section: SMU configuration
#                         ui.label('SMU Setup').style('font-size: 18px; font-weight: bold; margin-top: 0px;')
#                         self.smu_card = ui.card().style('margin-bottom: 10px; width: 950px;')
#                         self.sensor_type.on('update:model-value', lambda _: self.update_smu_setup_based_on_sensor_type())
#                         self.update_smu_setup_based_on_sensor_type()
                        
#             #Results Tab
#             with ui.tab_panel(resultsTab):
#                 self.results_section = ui.row()

#     # Updates the panel depending on the selected test type
#     @ui.refreshable
#     def update_test_type_params(self, test_type):
#         self.cond_params.clear()
#         if test_type == 'Linear':
#             with self.cond_params:
#                 ui.label('Linear Sweep Parameters').style('font-weight: bold;')
#                 self.lin_start = ui.number(value=0, min=0, max=10000, step=1, label='Start ppm').style('width: 150px;')
#                 self.lin_stop = ui.number(value=1000, min=0, max=10000, step=1, label='Stop ppm').style('width: 150px;')
#                 self.lin_step = ui.number(value=10, min=0.1, max=1000, step=0.1, label='Step ppm').style('width: 150px;')
#         elif test_type == 'Pulse':
#             with self.cond_params:
#                 ui.label('Pulse Test Parameters').style('font-weight: bold;')
#                 self.pulse_ppm = ui.number(value=500, min=0, max=10000, step=1, label='Pulse ppm').style('width: 150px;')
#                 self.pulse_count = ui.number(value=5, min=1, max=100, step=1, label='Pulse Count').style('width: 150px;')
#         elif test_type == 'Custom':
#             with self.cond_params:
#                 ui.label('Custom Test Parameters').style('font-weight: bold;')
#                 self.custom_ppm_list = ui.textarea(placeholder='Comma separated ppm values, e.g. 400,200,600').style('width: 300px; height: 130px;')
    
#     def update_smu_setup_based_on_sensor_type(self):
#         current_ranges = {
#             'Autorange': 1,  # handled separately
#             '200 mA': 0.2,
#             '20 mA': 0.02,
#             '2 mA': 0.002,
#             '200 µA': 0.0002,
#             '20 µA': 0.00002
#         }
#         unit_scaling = {
#             '200 mA': ('mA', 1e3),
#             '20 mA': ('mA', 1e3),
#             '2 mA': ('mA', 1e3),
#             '200 µA': ('µA', 1e6),
#             '20 µA': ('µA', 1e6)
#         }
#         sampling_rates = [str(v) for v in [64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]]
#         self.smu_card.clear()
#         self.sensor_config = []

#         with self.smu_card:
#             with ui.row().classes('font-bold'):
#                 ui.markdown('Enable').style('width: 60px;')
#                 ui.markdown('SMU-CH(s)').style('width: 100px;')
#                 ui.markdown('Name').style('width: 80px;')
#                 if self.sensor_type.value == 'Transistor':
#                     ui.markdown('V<sub>D</sub> [CH1]').style('width: 60px;')
#                     ui.markdown('V<sub>G</sub> [CH2] Start').style('width: 60px;')
#                     ui.markdown('V<sub>G</sub> [CH2] Stop').style('width: 60px;')
#                     ui.markdown('V<sub>G</sub> [CH2] Step').style('width: 60px;')
#                 else:
#                     ui.markdown('V Out').style('width: 60px;')
#                     ui.markdown('V Lim').style('width: 60px;')
#                 ui.markdown('I Range').style('width: 90px;')
#                 ui.markdown('I Lim').style('width: 90px;')
#                 ui.markdown('Sampling Rate').style('width: 70px;')

#             self.sensor_config = []

#             if self.sensor_type.value == 'Transistor':
#                 for i in range(0, 8, 2):
#                     smu = f"SMU{(i//2)+1}"
#                     smu_ch1 = f"SMU{(i//2)+1}-CH1"
#                     smu_ch2 = f"SMU{(i//2)+1}-CH2"
#                     with ui.row().style('margin-bottom: 4px; align-items: center;'):
#                         enabled = ui.checkbox(value=False)
#                         smu_label = ui.label(f'{smu_ch1}, {smu_ch2}').style('width: 100px; font-weight: bold;')
#                         sensor_name = ui.input(placeholder=f'Sensor {i//2+1}', value=f'Sensor {i//2+1}').style('width: 100px;')

#                         v_drain = ui.number(value=1.0, min=0, max=10, step=0.1).style('width: 60px;')
#                         v_gate_start = ui.number(value=0.0, min=0, max=10, step=0.1).style('width: 60px;')
#                         v_gate_stop = ui.number(value=2.0, min=0, max=10, step=0.1).style('width: 60px;')
#                         v_gate_step = ui.number(value=0.1, min=0.01, max=1, step=0.01).style('width: 60px;')

#                         i_range_select = ui.select(options=list(current_ranges.keys()), value='200 mA').style('width: 90px;')
#                         default_range_label = i_range_select.value
#                         default_unit, default_multiplier = unit_scaling[default_range_label] if default_range_label != 'Autorange' else ('', 1)
#                         default_max = current_ranges[default_range_label] * default_multiplier if default_range_label != 'Autorange' else 0

#                         i_limit = ui.number(value=default_max, min=0, max=default_max, step=1).style('width: 60px;')
#                         i_limit_label = ui.label(f'({default_unit})').style('margin-left: -10px; width: 30px;')

#                         def update_limit(e, limit_widget=i_limit, unit_label=i_limit_label):
#                             label = e.args['label']
#                             if label == 'Autorange':
#                                 limit_widget.disable()
#                                 unit_label.set_text('')
#                                 return
#                             limit_widget.enable()
#                             unit, scale = unit_scaling[label]
#                             max_value = current_ranges[label] * scale
#                             limit_widget.set_value(max_value)
#                             limit_widget.props['max'] = max_value
#                             limit_widget.props['step'] = max_value / 100
#                             limit_widget.update()
#                             unit_label.set_text(f'({unit})')

#                         i_range_select.on('update:model-value', update_limit)

#                         sampling = ui.select(options=sampling_rates, value='1024').style('width: 70px;')

#                         self.sensor_config.append({
#                             'enabled': enabled,
#                             'name': sensor_name,
#                             'smu': smu,
#                             'channel': 'CH1-CH2',
#                             'v_drain': v_drain,
#                             'v_gate_start': v_gate_start,
#                             'v_gate_stop': v_gate_stop,
#                             'v_gate_step': v_gate_step,
#                             'i_range': i_range_select,
#                             'i_limit': i_limit,
#                             'sampling': sampling
#                         })
#             else:
#                 for i in range(8):
#                     smu = f"SMU{(i//2)+1}"
#                     ch = f"CH{(i%2)+1}"
#                     with ui.row().style('margin-bottom: 4px; align-items: center;'):
#                         enabled = ui.checkbox(value=False)
#                         smu_label = ui.label(f'{smu}-{ch}').style('width: 100px; font-weight: bold;')
#                         sensor_name = ui.input(placeholder=f'Sensor {i+1}', value=f'Sensor {i+1}').style('width: 100px;')
#                         v_out = ui.number(value=0.0, min=-10, max=10, step=0.1).style('width: 60px;')
#                         v_lim = ui.number(value=10.0, min=0, max=10, step=0.1).style('width: 60px;')

#                         i_range_select = ui.select(options=list(current_ranges.keys()), value='200 mA').style('width: 90px;')
#                         default_range_label = i_range_select.value
#                         default_unit, default_multiplier = unit_scaling[default_range_label] if default_range_label != 'Autorange' else ('', 1)
#                         default_max = current_ranges[default_range_label] * default_multiplier if default_range_label != 'Autorange' else 0

#                         i_limit = ui.number(value=default_max, min=0, max=default_max, step=1).style('width: 60px;')
#                         i_limit_label = ui.label(f'({default_unit})').style('margin-left: -10px; width: 30px;')

#                         def update_limit(e, limit_widget=i_limit, unit_label=i_limit_label):
#                             label = e.args['label']
#                             if label == 'Autorange':
#                                 limit_widget.disable()
#                                 unit_label.set_text('')
#                                 return
#                             limit_widget.enable()
#                             unit, scale = unit_scaling[label]
#                             max_value = current_ranges[label] * scale
#                             limit_widget.set_value(max_value)
#                             limit_widget.props['max'] = max_value
#                             limit_widget.props['step'] = max_value / 100
#                             limit_widget.update()
#                             unit_label.set_text(f'({unit})')

#                         i_range_select.on('update:model-value', update_limit)

#                         sampling = ui.select(options=sampling_rates, value='1024').style('width: 70px;')

#                         self.sensor_config.append({
#                             'enabled': enabled,
#                             'name': sensor_name,
#                             'smu': smu,
#                             'channel': ch,
#                             'v_out': v_out,
#                             'v_lim': v_lim,
#                             'i_range': i_range_select,
#                             'i_limit': i_limit,
#                             'sampling': sampling
#                         })

#     #Functions to update the preview plot 
#     def update_preview_plot(self):
#         stab_time = self.stab_time.value
#         expo_time = self.expo_time.value
#         rec_time = self.rec_time.value
        
#         x_data = []
#         y_data = []
#         t = 0

#         if self.test_type.value == 'Linear':
#             start = self.lin_start.value
#             stop = self.lin_stop.value
#             step = self.lin_step.value
#             t += stab_time
#             x_data.append(t)   # Stabilization
#             y_data.append(0)
#             for ppm in range(int(start), int(stop + 1), int(step)):
#                 t += expo_time
#                 x_data.append(t)   # Exposure
#                 y_data.append(ppm)
#                 t += rec_time
#                 x_data.append(t)   # Step
#                 y_data.append(0)
               
#         elif self.test_type.value == 'Pulse':
#             pulse_ppm = self.pulse_ppm.value
#             pulse_count = self.pulse_count.value
#             t += stab_time
#             x_data.append(t)   # Stabilization
#             y_data.append(0)
#             for _ in range(int(pulse_count)):
#                 t += expo_time
#                 x_data.append(t)   # Exposure
#                 y_data.append(pulse_ppm)
#                 t += rec_time
#                 x_data.append(t)   # Step
#                 y_data.append(0)
                
#         elif self.test_type.value == 'Custom':
#             try:
#                 ppm_values = [int(v.strip()) for v in self.custom_ppm_list.value.split(',') if v.strip()]
#             except ValueError:
#                 ui.notify('Invalid input in Custom PPM list.', type='negative')
#                 return
#             t += stab_time
#             x_data.append(t)   # Stabilization
#             y_data.append(0)
#             for ppm in ppm_values:
#                 t += expo_time
#                 x_data.append(t)   # Exposure
#                 y_data.append(ppm)
#                 t += rec_time
#                 x_data.append(t)   # Step
#                 y_data.append(0)
                
#         # Update echart
#         self.preview_plot.options['xAxis']['type'] = 'value'
#         self.preview_plot.options['xAxis']['name'] = 'Time (m)'
#         self.preview_plot.options['xAxis']['axisLabel'] = {'formatter': '{value}'}
#         self.preview_plot.options['yAxis']['name'] = 'ppm'
#         self.preview_plot.options['series'] = [{
#             'type': 'line',
#             'step': 'start',
#             'data': list(zip(x_data, y_data)),
#             'name': 'PPM',
#             'areaStyle': {}  
#         }]
#         self.preview_plot.update()
    
#     # To gather all inputs from GUI widgets into a dict
#     def collect_config(self):
#         config = {
#             'carrier_gas_ao': self.carrier_gas_analogOut.value,
#             'target_gas_ao': self.target_gas_analogOut.value,
#             'interfering_gas_ao': self.interfering_gas_analogOut.value,
#         }
#         return config
    
#     def update_results_layout(self):
#         self.results_state = {}
#         self.results_section.clear()
#         if self.sensor_type.value == 'Resistor':
#             with self.results_section:
#                 with ui.grid(columns=4).style('gap: 20px;'):
#                     for i, config in enumerate(self.sensor_config):
#                         if not config['enabled'].value:
#                              continue
#                         sensor_name = config['name'].value
#                         with ui.card().style('width: 380px; margin: 1%;  display: inline-block; padding: 10px;'):
#                             ui.label(f'{sensor_name}').style('font-weight: bold; font-size: 16px; margin-bottom: 5px;')
#                             # Temperature and humidity
#                             temp_label = ui.label('Temp: -- °C').style('font-size: 14px;')
#                             rh_label = ui.label('Humidity: -- %RH').style('font-size: 14px;')

#                             # Dual Y-axis plot (Resistance vs Time + PPM)
#                             chart = ui.echart({
#                                 'tooltip': {'trigger': 'axis'},
#                                 'xAxis': {'type': 'value', 'name': 't (s)'},
#                                 'yAxis': [
#                                     {'type': 'value', 'name': 'R(Ω)', 'position': 'left'},
#                                     {'type': 'value', 'name': 'PPM', 'position': 'right'}
#                                 ],
#                                 'series': [
#                                     {'name': 'R(Ω)', 'type': 'line', 'yAxisIndex': 0, 'data': []},
#                                     {'name': 'PPM', 'type': 'line', 'yAxisIndex': 1, 'data': []}
#                                 ],
#                                 'legend': {'data': ['R(Ω)', 'PPM']}
#                             }).style('width: 100%; height: 400px; margin-top: 5px;')

#                             # CSV Export
#                             ui.button('Export CSV', icon='download', on_click=lambda s=sensor_name: self.export_csv(s)).style('margin-top: 0px; width: 100%;')

#                             # Save the widgets for real-time updates
#                             self.results_state[sensor_name] = {
#                                 'temp_label': temp_label,
#                                 'rh_label': rh_label,
#                                 'chart': chart,
#                                 'data': []  # Optional: store [t, R, PPM, T, RH] here for CSV
#                             }

#         elif self.sensor_type.value == 'Transistor':
#             with self.results_section:
#                 with ui.grid(columns=4).style('gap: 20px;'):
#                     for i, config in enumerate(self.sensor_config):
#                         if not config['enabled'].value:
#                             continue
#                         sensor_name = config['name'].value
#                         with ui.card().style('width: 380px; margin: 1%;  display: inline-block; padding: 10px;'):
#                             ui.label(f'{sensor_name}').style('font-weight: bold; font-size: 16px; margin-bottom: 5px;')
#                             # Temperature and humidity
#                             temp_label = ui.label('Temp: -- °C').style('font-size: 14px;')
#                             rh_label = ui.label('Humidity: -- %RH').style('font-size: 14px;')
#                             chart = ui.echart({
#                                 'tooltip': {'trigger': 'axis'},
#                                 'xAxis': {'type': 'value', 'name': 'VG (V)'},
#                                 'yAxis': {'type': 'value', 'name': 'ID (A)'},        #changes
#                                 'series': [{'name': 'ID-VG', 'type': 'line', 'data': []}],
#                                 'legend': {'data': ['ID-VG']}
#                             }).style('width: 100%; height: 400px; margin-top: 5px;')

#                             ui.button('Export CSV', icon='download', on_click=lambda s=sensor_name: self.export_csv(s)).style('margin-top: 0px; width: 100%;')

#                             self.results_state[sensor_name] = {
#                                 'chart': chart,
#                                 'data': []  # Optional: store [VG, ID] here
#                             }


#         elif self.sensor_type.value == 'Diode':
#             with self.results_section:
#                 ui.label('Diode plot logic to be added here...')

#     def export_csv(self, sensor_name):
#         if sensor_name not in self.results_state:
#             ui.notify(f"No data found for sensor: {sensor_name}", type='warning')
#             return

#         data = self.results_state[sensor_name]['data']
#         if not data:
#             ui.notify(f"No data to export for sensor: {sensor_name}", type='warning')
#             return

#         filename = f'{sensor_name.replace(" ", "_")}_results.csv'
#         filepath = Path('results') / filename
#         filepath.parent.mkdir(exist_ok=True)

#         # Write CSV
#         with open(filepath, mode='w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Time (s)', 'Resistance (Ω)', 'PPM', 'Temperature (°C)', 'Humidity (%RH)'])
#             writer.writerows(data)

#         ui.notify(f'Data exported: {filepath}', type='positive')

#     # Runs the experiment simulation
#     async def run_experiment(self):
#         self.status_label.set_text('Status: Running...')
#         self.start_btn.disable()
#         self.stop_btn.enable()
#         self.running = True
#         total_steps = 100

#         for step in range(total_steps + 1):
#             if not self.running:
#                 break

#             t = step  # time value

#             # Loop over sensors
#             for sensor_name, widgets in self.results_state.items():
#                 if self.sensor_type.value == 'Transistor':
#                     vg = round(step * 0.05, 2)  # Simulate VG sweep
#                     id_current = round(1e-6 * (vg ** 2) + random.uniform(-1e-7, 1e-7), 8)  # Simulate quadratic ID

#                     chart = widgets['chart']
#                     chart.options['series'][0]['data'].append([vg, id_current])
#                     chart.update()

#                     widgets['data'].append([vg, id_current])

#                 # Simulated values – replace these with actual measurements
#                 t = step
#                 resistance = round(1e5 + 5000 * random.uniform(-1, 1), 2)
#                 ppm = round(400 + 50 * random.uniform(-1, 1), 2)
#                 temp = round(25 + random.uniform(-1, 1), 2)
#                 rh = round(50 + random.uniform(-5, 5), 2)

#                 widgets['temp_label'].set_text(f'Temp: {temp} °C')
#                 widgets['rh_label'].set_text(f'Humidity: {rh} %RH')

#                 chart = widgets['chart']
#                 chart.options['series'][0]['data'].append([t, resistance])
#                 chart.options['series'][1]['data'].append([t, ppm])
#                 chart.update()

#                 # Save for CSV
#                 widgets['data'].append([t, resistance, ppm, temp, rh])

#             self.progress_bar.value = step
#             await asyncio.sleep(0.1)

#         self.status_label.set_text('Status: Finished')
#         self.start_btn.enable()
#         self.stop_btn.disable()
#         self.running = False

#     # Starts the experiment
#     def start_experiment(self):
#         if self.running:
#             return
#         ######Error Checking for Analog Output Assignments########
#         # Collect AO assignments
#         ao_assignments = {
#             'Carrier Gas': self.carrier_gas_analogOut.value,
#             'Target Gas': self.target_gas_analogOut.value,
#             'Interfering Gas': self.interfering_gas_analogOut.value
#         }
#         # Check if any AO is 'None'
#         if 'None' in ao_assignments.values():
#             self.status_label.set_text('Error: All gases must be assigned to an AO.')
#             ui.notify('Please assign a valid AO (AO0, AO1, AO2) to each gas.', type='negative')
#             return
#         # Check for duplicates
#         assigned_aos = list(ao_assignments.values())
#         if len(assigned_aos) != len(set(assigned_aos)):
#             self.status_label.set_text('Error: Duplicate AO assignments detected.')
#             ui.notify('Each gas must be assigned to a unique AO.', type='negative')
#             return
#         #Call the function to debug the parameters, it can be commented later if debbuging is not necessary
#         self.print_user_parameters()
#         #Call the function to update the layout of the results tab
#         self.update_results_layout()
#         # Passed validation: run experiment
#         asyncio.create_task(self.run_experiment())

#     # Stops the experiment
#     def stop_experiment(self):
#         self.running = False
#         self.status_label.set_text('Status: Stopped by user')
#         self.start_btn.enable()
#         self.stop_btn.disable()
    
#     #Debugging of the user input parameters in terminal
#     def print_user_parameters(self):
#         print('\n--- USER PARAMETERS ---')
#         print(f'Carrier Gas:')
#         print(f'  AO: {self.carrier_gas_analogOut.value}')
#         print(f'  Initial ppm: {self.carrier_gas_initialppm.value}')
#         print(f'  Max Flow: {self.carrier_gas_maxflow.value}')
#         print(f'Target Gas:')
#         print(f'  AO: {self.target_gas_analogOut.value}')
#         print(f'  Initial ppm: {self.target_gas_initialppm.value}')
#         print(f'  Max Flow: {self.target_gas_maxflow.value}')
#         print(f'Interfering Gas:')
#         print(f'  AO: {self.interfering_gas_analogOut.value}')
#         print(f'  Initial ppm: {self.interfering_gas_initialppm.value}')
#         print(f'  Max Flow: {self.interfering_gas_maxflow.value}')

#         print(f'\nTiming Setup:')
#         print(f'  Stabilization Time: {self.stab_time.value} m')
#         print(f'  Exposure Time: {self.expo_time.value} m')
#         print(f'  Recovery Time: {self.rec_time.value} m')

#         print(f'\nSensor Type: {self.sensor_type.value}')
        
#         print(f'\nTest Type: {self.test_type.value}')
#         if self.test_type.value == 'Linear':
#             print(f'  Start ppm: {self.lin_start.value}')
#             print(f'  Stop ppm: {self.lin_stop.value}')
#             print(f'  Step ppm: {self.lin_step.value}')
#         elif self.test_type.value == 'Pulse':
#             print(f'  Pulse ppm: {self.pulse_ppm.value}')
#             print(f'  Pulse Count: {self.pulse_count.value}')
#         elif self.test_type.value == 'Custom':
#             print(f'  Custom ppm List: {self.custom_ppm_list.value}')

#         print(f'\nSMU Setup:')
#         current_ranges_map = {
#             'Autorange': 1.0,
#             '200 mA': 0.2,
#             '20 mA': 0.02,
#             '2 mA': 0.002,
#             '200 µA': 0.0002,
#             '20 µA': 0.00002
#         }

#         unit_scaling = {
#             '200 mA': ('mA', 1e-3),
#             '20 mA': ('mA', 1e-3),
#             '2 mA': ('mA', 1e-3),
#             '200 µA': ('µA', 1e-6),
#             '20 µA': ('µA', 1e-6),
#             'Autorange': ('Auto', 1)
#         }

#         for i, config in enumerate(self.sensor_config, start=1):
#             if config['enabled'].value:
#                 smu_ch = f"{config['smu']}-{config['channel']}"
#                 name = config['name'].value
#                 i_range_label = config['i_range'].value
#                 i_lim_display = config['i_limit'].value
#                 sampling = config['sampling'].value

#                 print(f'  Sensor {i}: {name}')
#                 print(f'    SMU-CH: {smu_ch}')
#                 if 'v_drain' in config:
#                     v_drain = config['v_drain'].value
#                     v_gate_start = config['v_gate_start'].value
#                     v_gate_stop = config['v_gate_stop'].value
#                     v_gate_step = config['v_gate_step'].value
#                     print(f'    Drain Voltage: {v_drain} V')
#                     print(f'    Gate Sweep: Start={v_gate_start} V, Stop={v_gate_stop} V, Step={v_gate_step} V')
#                 else:
#                     v_out = config['v_out'].value
#                     v_lim = config['v_lim'].value
#                     print(f'    V Out: {v_out} V')
#                     print(f'    V Lim: {v_lim} V')
#                 if i_range_label == 'Autorange':
#                     print(f'    I Range: Autorange (handled automatically by SMU)')
#                     print(f'    I Lim: N/A (limit ignored in autorange mode)')
#                 else:
#                     i_range_amp = current_ranges_map[i_range_label]
#                     _, scale = unit_scaling[i_range_label]
#                     i_lim_amp = i_lim_display * scale
#                     print(f'    I Range: {i_range_amp} A (user input: {i_range_label})')
#                     print(f'    I Lim: {i_lim_amp} A (user input: {i_lim_display} {i_range_label[-2:]})')

#                 print(f'    Sampling Rate: {sampling}')

# # Runs the app
# if __name__ in {"__main__", "__mp_main__"}:
#     app = GasSensorApp()
#     ui.run(port=8090)

# # drain current verses gate voltage
# # simulating the plot update_sensors
# # simulate vgs from 0 to 5 volts, in the logic file
# # simulate vgs and the id
# #variables and names of the plot

# #diode same as resistor, measure the current instead of resistance
# #logic same as resistor

from nicegui import ui
import asyncio
import matplotlib
import random
import csv
from pathlib import Path
from logic import get_sensor_data
from logic import calculate_gas_flows, flow_to_voltage, set_analog_output
import u6


# Main GUI class
class GasSensorApp:
    def __init__(self):
        try:
            self.labjack = u6.U6()
            labjack_status = True
        except Exception as e:
            print(f"LabJack connection failed: {e}")
            self.labjack = None
            labjack_status = False

        self.running = False
        dark = ui.dark_mode()
        ui.switch('Dark mode').bind_value(dark)
        ui.label('Gas Sensor Characterization Platform').style('font-size: 22px; font-weight: bold; margin-bottom: 0px;').classes('text-center')
        
        with ui.column().style('align-items: center; margin-top: 30px; gap: 10px;'):
            # Start and stop buttons
            with ui.row().style('gap: 20px;'):
                def handle_start_click():
                    self.start_experiment()
                    tabs.set_value('Results')

                self.start_btn = ui.button('Start', on_click=handle_start_click).style('width: 120px;')
                self.stop_btn = ui.button('Stop', on_click=self.stop_experiment).style('width: 120px;')
                self.stop_btn.disable()

            # Status indicators
            self.status_label = ui.label('Status: Idle').style('margin-top: 10px;')
            self.labjack_label = ui.label().style('margin-top: 5px;')

            if labjack_status:
                self.labjack_label.set_text("LabJack: Connected")
                self.labjack_label.style("color: green")
            else:
                self.labjack_label.set_text("LabJack: Disconnected")
                self.labjack_label.style("color: red")
                
        with ui.tabs() as tabs:
            setupTab = ui.tab('Environment Setup')
            testTab = ui.tab('Test Setup')
            smuTab = ui.tab('Gas Sensors Setup')
            resultsTab = ui.tab('Results')
        
        with ui.tab_panels(tabs, value=setupTab):
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
                            for mfc_label in ['Carrier Gas', 'Target Gas', 'Interfering Gas']:
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
                                            f'{mfc_label.lower().replace(" ", "_")}_maxflow',
                                            ui.number(
                                                value=0, min=0, max=10000, step=1
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
                        self.smu_card = ui.card().style('margin-bottom: 10px; width: 950px;')
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
                ui.markdown('Enable').style('width: 60px;')
                ui.markdown('SMU-CH(s)').style('width: 100px;')
                ui.markdown('Name').style('width: 80px;')
                if self.sensor_type.value == 'Transistor':
                    ui.markdown('V<sub>D</sub> [CH1]').style('width: 60px;')
                    ui.markdown('V<sub>G</sub> [CH2] Start').style('width: 60px;')
                    ui.markdown('V<sub>G</sub> [CH2] Stop').style('width: 60px;')
                    ui.markdown('V<sub>G</sub> [CH2] Step').style('width: 60px;')
                else:
                    ui.markdown('V Out').style('width: 60px;')
                    ui.markdown('V Lim').style('width: 60px;')
                ui.markdown('I Range').style('width: 90px;')
                ui.markdown('I Lim').style('width: 90px;')
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
                        sensor_name = ui.input(placeholder=f'Sensor {i//2+1}', value=f'Sensor {i//2+1}').style('width: 100px;')

                        v_drain = ui.number(value=1.0, min=0, max=10, step=0.1).style('width: 60px;')
                        v_gate_start = ui.number(value=0.0, min=0, max=10, step=0.1).style('width: 60px;')
                        v_gate_stop = ui.number(value=2.0, min=0, max=10, step=0.1).style('width: 60px;')
                        v_gate_step = ui.number(value=0.1, min=0.01, max=1, step=0.01).style('width: 60px;')

                        i_range_select = ui.select(options=list(current_ranges.keys()), value='200 mA').style('width: 90px;')
                        default_range_label = i_range_select.value
                        default_unit, default_multiplier = unit_scaling[default_range_label] if default_range_label != 'Autorange' else ('', 1)
                        default_max = current_ranges[default_range_label] * default_multiplier if default_range_label != 'Autorange' else 0

                        i_limit = ui.number(value=default_max, min=0, max=default_max, step=1).style('width: 60px;')
                        i_limit_label = ui.label(f'({default_unit})').style('margin-left: -10px; width: 30px;')

                        def update_limit(e, limit_widget=i_limit, unit_label=i_limit_label):
                            label = e.args['label']
                            if label == 'Autorange':
                                limit_widget.disable()
                                unit_label.set_text('')
                                return
                            limit_widget.enable()
                            unit, scale = unit_scaling[label]
                            max_value = current_ranges[label] * scale
                            limit_widget.set_value(max_value)
                            limit_widget.props['max'] = max_value
                            limit_widget.props['step'] = max_value / 100
                            limit_widget.update()
                            unit_label.set_text(f'({unit})')

                        i_range_select.on('update:model-value', update_limit)

                        sampling = ui.select(options=sampling_rates, value='1024').style('width: 70px;')

                        self.sensor_config.append({
                            'enabled': enabled,
                            'name': sensor_name,
                            'smu': smu,
                            'channel': 'CH1-CH2',
                            'v_drain': v_drain,
                            'v_gate_start': v_gate_start,
                            'v_gate_stop': v_gate_stop,
                            'v_gate_step': v_gate_step,
                            'i_range': i_range_select,
                            'i_limit': i_limit,
                            'sampling': sampling
                        })
            else:
                for i in range(8):
                    smu = f"SMU{(i//2)+1}"
                    ch = f"CH{(i%2)+1}"
                    with ui.row().style('margin-bottom: 4px; align-items: center;'):
                        enabled = ui.checkbox(value=False)
                        smu_label = ui.label(f'{smu}-{ch}').style('width: 100px; font-weight: bold;')
                        sensor_name = ui.input(placeholder=f'Sensor {i+1}', value=f'Sensor {i+1}').style('width: 100px;')
                        v_out = ui.number(value=0.0, min=-10, max=10, step=0.1).style('width: 60px;')
                        v_lim = ui.number(value=10.0, min=0, max=10, step=0.1).style('width: 60px;')

                        i_range_select = ui.select(options=list(current_ranges.keys()), value='200 mA').style('width: 90px;')
                        default_range_label = i_range_select.value
                        default_unit, default_multiplier = unit_scaling[default_range_label] if default_range_label != 'Autorange' else ('', 1)
                        default_max = current_ranges[default_range_label] * default_multiplier if default_range_label != 'Autorange' else 0

                        i_limit = ui.number(value=default_max, min=0, max=default_max, step=1).style('width: 60px;')
                        i_limit_label = ui.label(f'({default_unit})').style('margin-left: -10px; width: 30px;')

                        def update_limit(e, limit_widget=i_limit, unit_label=i_limit_label):
                            label = e.args['label']
                            if label == 'Autorange':
                                limit_widget.disable()
                                unit_label.set_text('')
                                return
                            limit_widget.enable()
                            unit, scale = unit_scaling[label]
                            max_value = current_ranges[label] * scale
                            limit_widget.set_value(max_value)
                            limit_widget.props['max'] = max_value
                            limit_widget.props['step'] = max_value / 100
                            limit_widget.update()
                            unit_label.set_text(f'({unit})')

                        i_range_select.on('update:model-value', update_limit)

                        sampling = ui.select(options=sampling_rates, value='1024').style('width: 70px;')

                        self.sensor_config.append({
                            'enabled': enabled,
                            'name': sensor_name,
                            'smu': smu,
                            'channel': ch,
                            'v_out': v_out,
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
            'totalFlow' : 2000,
            'test_type': self.test_type.value,
            'stab_time': self.stab_time.value,
            'expo_time': self.expo_time.value,
            'rec_time': self.rec_time.value,
            'sensor_type': self.sensor_type.value,
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
            with self.results_section:
                with ui.grid(columns=4).style('gap: 20px;'):
                    for i, config in enumerate(self.sensor_config):
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
                            ui.button('Export CSV', icon='download', on_click=lambda s=sensor_name: self.export_csv(s)).style('margin-top: 0px; width: 100%;')

                            # Save the widgets for real-time updates
                            self.results_state[sensor_name] = {
                                'temp_label': temp_label,
                                'rh_label': rh_label,
                                'chart': chart,
                                'data': []  # Optional: store [t, R, PPM, T, RH] here for CSV
                            }

        elif self.sensor_type.value == 'Transistor':
            with self.results_section:
                with ui.grid(columns=4).style('gap: 20px;'):
                    for i, config in enumerate(self.sensor_config):
                        if not config['enabled'].value:
                            continue
                        sensor_name = config['name'].value
                        with ui.card().style('width: 380px; margin: 1%; display: inline-block; padding: 10px;'):
                            ui.label(f'{sensor_name}').style('font-weight: bold; font-size: 16px; margin-bottom: 5px;')
                            temp_label = ui.label('Temp: -- °C').style('font-size: 14px;')
                            rh_label   = ui.label('Humidity: -- %RH').style('font-size: 14px;')

                            chart = ui.echart({
                                'tooltip': {'trigger': 'axis'},
                                'xAxis':   {'type': 'value', 'name': 'VG (V)'},
                                'yAxis':   {'type': 'value', 'name': 'ID (A)'},
                                'series':  [{'name': 'ID–VG', 'type': 'line', 'data': []}],
                                'legend':  {'data': ['ID–VG']}
                            }).style('width: 100%; height: 400px; margin-top: 5px;')

                            ui.button('Export CSV', icon='download', on_click=lambda s=sensor_name: self.export_csv(s)) \
                            .style('margin-top: 0px; width: 100%;')

                            self.results_state[sensor_name] = {
                                'temp_label': temp_label,
                                'rh_label':   rh_label,
                                'chart':      chart,
                                'data':       []
                            }





        elif self.sensor_type.value == 'Diode':
            with self.results_section:
                with ui.grid(columns=4).style('gap: 20px;'):
                    for i, config in enumerate(self.sensor_config):
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
                            ui.button('Export CSV', icon='download', on_click=lambda s=sensor_name: self.export_csv(s)).style('margin-top: 0px; width: 100%;')

                            # Save the widgets for real-time updates
                            self.results_state[sensor_name] = {
                                'temp_label': temp_label,
                                'rh_label': rh_label,
                                'chart': chart,
                                'data': []  # Optional: store [t, R, PPM, T, RH] here for CSV
                            }


    def export_csv(self, sensor_name):
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
            writer.writerow(['Time (s)', 'Resistance (Ω)', 'PPM', 'Temperature (°C)', 'Humidity (%RH)'])
            writer.writerows(data)

        ui.notify(f'Data exported: {filepath}', type='positive')

    async def update_sensors(self, config, step, phase, ppm):
        sensor_type = config['sensor_type']

        for sensor_name, widgets in self.results_state.items():
            data = get_sensor_data(sensor_type, ppm)

            # Update environment labels
            widgets['temp_label'].set_text(f"Temp: {data['temp']} °C")
            widgets['rh_label'].set_text(f"Humidity: {data['rh']} %RH")

            chart = widgets['chart']

            if sensor_type == 'Resistor':
                resistance = data['resistance']
                chart.options['series'][0]['data'].append([step, resistance])
                chart.options['series'][1]['data'].append([step, ppm])
                chart.update()
                widgets['data'].append([step, resistance, ppm, data['temp'], data['rh']])

            elif sensor_type == 'Transistor':
                vgs    = data['vgs']
                id_val = data['id']
                # append a single (VG, ID) point
                chart.options['series'][0]['data'].append([vgs, id_val])
                chart.update()
                widgets['data'].append([vgs, id_val, ppm, data['temp'], data['rh']])

                vgs    = data['vgs']
                id_val = data['id']

                # push a point (VG, ID) to our single series
                chart.options['series'][0]['data'].append([vgs, id_val])
                chart.update()

                # save for CSV if you like
                widgets['data'].append([vgs, id_val, ppm, data['temp'], data['rh']])
                
            elif sensor_type == 'Transistor':
                # pull out gate‑voltage and drain‑current
                    vgs    = data['vgs']
                    id_val = data['id']

                # append exactly one point [VG, ID] to the single series
                    chart.options['series'][0]['data'].append([vgs, id_val])
                    chart.update()

                # also save to your CSV buffer
                    widgets['data'].append([vgs, id_val, ppm, data['temp'], data['rh']])



    # Runs the experiment simulation
    async def run_experiment(self):
        self.start_btn.disable()
        self.stop_btn.enable()

        config = self.experiment_config  # User parameters

        def frange(start, stop, step):
            while start <= stop:
                yield round(start, 4)
                start += step

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

        sim_unit = 1 # 60 for minutes, 1 for seconds
        # Timing logic convert minutes to steps
        stab_steps = int(config['stab_time'] * sim_unit / 0.1)  # Using a 0.1s resolution, 10Hz
        expo_steps = int(config['expo_time'] * sim_unit / 0.1)
        rec_steps  = int(config['rec_time']  * sim_unit / 0.1)

        self.running = True
        self.status_label.set_text("Status: Stabilization time...")
        for step in range(stab_steps):
            if not self.running:
                break
            await self.update_sensors(config, step, 'stabilization', 0)
            self.progress_bar.value = step
            await asyncio.sleep(0.1)

        total_phase = len(sequence)
        current_step = stab_steps

        for i, ppm in enumerate(sequence):
            if not self.running:
                break
            # Exposure
            self.status_label.set_text(f"Status: Exposure ({i+1}/{total_phase}) - {ppm} ppm")
            #apply_mfc_target_ppm(ppm)  # Call the function to run the mfc (this has to be in the logic.py)
            flows = calculate_gas_flows(ppm, config)
            target_flow_setpoint = flows['target_flow']
            carrier_flow_setpoint = flows['carrier_flow']
            # Convert to initial voltages
            v_target = flow_to_voltage(target_flow_setpoint, config['target_gas_maxFlow'])
            v_carrier = flow_to_voltage(carrier_flow_setpoint, config['carrier_gas_maxFlow'])
            #Apply voltages to the MFC
            set_analog_output(self.labjack, config['target_gas_ao'], v_target)
            set_analog_output(self.labjack, config['carrier_gas_ao'], v_carrier)

                # … after stabilization …

        # --- start of transistor‐specific sweep ---
        if config['sensor_type'] == 'Transistor':
            # helper to step floats
            def frange(start, stop, step):
                x = start
                while x <= stop:
                    yield round(x, 4)
                    x += step

            for vgs in frange(config['v_gate_start'],
                            config['v_gate_stop'],
                            config['v_gate_step']):
                if not self.running:
                    break
                # simulate data (override your stub's vgs)
                data = get_sensor_data('Transistor', ppm=0)
                data['vgs'] = vgs

                # plot one (Vg, Id) point
                for widgets in self.results_state.values():
                    chart   = widgets['chart']
                    id_val  = data['id']
                    chart.options['series'][0]['data'].append([vgs, id_val])
                    chart.update()
                    widgets['data'].append([vgs, id_val, data['temp'], data['rh']])

                await asyncio.sleep(0.1)
            # after sweep, you can jump straight to finish or do a short recovery
            self.running = False
            self.status_label.set_text("Status: Finished")
            self.start_btn.enable()
            self.stop_btn.disable()
            return
        # --- end of transistor sweep ---

        # … your original exposure & recovery loops for Resistor go here …


    # Starts the experiment
    def start_experiment(self):
        if self.running:
            return
        ######Error Checking for Analog Output Assignments########
        # Collect AO assignments
        ao_assignments = {
            'Carrier Gas': self.carrier_gas_analogOut.value,
            'Target Gas': self.target_gas_analogOut.value,
            'Interfering Gas': self.interfering_gas_analogOut.value
        }
        # Check if any AO is 'None'
        if 'None' in ao_assignments.values():
            self.status_label.set_text('Error: All gases must be assigned to an AO.')
            ui.notify('Please assign a valid AO (AO0, AO1, AO2) to each gas.', type='negative')
            return
        # Check for duplicates
        assigned_aos = list(ao_assignments.values())
        if len(assigned_aos) != len(set(assigned_aos)):
            self.status_label.set_text('Error: Duplicate AO assignments detected.')
            ui.notify('Each gas must be assigned to a unique AO.', type='negative')
            return
        #Call the function to debug the parameters, it can be commented later if debbuging is not necessary
        self.print_user_parameters()
        #Call the function to update the layout of the results tab
        self.update_results_layout()
        #Call the function to collect all the user parameters
        self.experiment_config = self.collect_config()

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

                print(f'  Sensor {i}: {name}')
                print(f'    SMU-CH: {smu_ch}')
                if 'v_drain' in config:
                    v_drain = config['v_drain'].value
                    v_gate_start = config['v_gate_start'].value
                    v_gate_stop = config['v_gate_stop'].value
                    v_gate_step = config['v_gate_step'].value
                    print(f'    Drain Voltage: {v_drain} V')
                    print(f'    Gate Sweep: Start={v_gate_start} V, Stop={v_gate_stop} V, Step={v_gate_step} V')
                else:
                    v_out = config['v_out'].value
                    v_lim = config['v_lim'].value
                    print(f'    V Out: {v_out} V')
                    print(f'    V Lim: {v_lim} V')
                if i_range_label == 'Autorange':
                    print(f'    I Range: Autorange (handled automatically by SMU)')
                    print(f'    I Lim: N/A (limit ignored in autorange mode)')
                else:
                    i_range_amp = current_ranges_map[i_range_label]
                    _, scale = unit_scaling[i_range_label]
                    i_lim_amp = i_lim_display * scale
                    print(f'    I Range: {i_range_amp} A (user input: {i_range_label})')
                    print(f'    I Lim: {i_lim_amp} A (user input: {i_lim_display} {i_range_label[-2:]})')

                print(f'    Sampling Rate: {sampling}')

# Runs the app
if __name__ in {"__main__", "__mp_main__"}:
    app = GasSensorApp()
    ui.run(port=8090)



