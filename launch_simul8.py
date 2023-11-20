import win32com
from win32com import client
import time

agv_01 = r"C:\Users\Mohammad\Desktop\Projects\Simul8 AGV\agv_m5r3_01_v05.S8"


class EventHandler():
    # def OnS8SimulationEndRun(self):
    def S8SimulationEndRun(self):
        print("Results:")
        return

    def OnS8SimulationOpened(self):
    # def S8SimulationOpened(self):
        print(f"Model opened: {S8.FileName}")
        return

    # def OnS8SimulationReadyToClose(self):
    def S8SimulationReadyToClose(self):
        print("Closing...")
        return

print("Connecting...")
S8 = win32com.client.DispatchWithEvents("Simul8.S8Simulation", EventHandler)
# print(S8)

print("Opening...")
S8.Open(agv_01)
print(S8.SimSpeed)
S8.SimSpeed = 90
print(S8.SimSpeed)
S8.visible = True

# Run and close the simulation
print("Resetting...")
S8.ResetSim(1) # arguments?
print("Running...")
S8.RunSim(500)
time.sleep(2.0) # seconds
print("Simu ended")

S8.Close()
# S8.Quit()
# S8.StepSim()
print("Ending...")

# S8.Quit()
# S8 = None