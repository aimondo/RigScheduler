
import csv

f = open('rigs.txt','r')
r = csv.reader(f)
rig_list = list(r)
f.close()

f = open('wells.txt','r')
r = csv.reader(f)
well_list = list(r)
f.close()

## Sort wells based on ranking
well_list = sorted(well_list, key=lambda x: float(x[0]), reverse=False)

final_day = 1000

## Just to hold the rig status so we can pick them off the line during day progression and
## figure out which rigs drilled which well
class rig:

    def __init__(self,rig_no):
        self.wells_drilled = [] #Assign wells to this rig
        self.occupied = False #Is the rig currently drilling another well?
        self.days_left = 0
        self.name = 'Rig ' + str(rig_no)

days = 0
rig_timeline = 0
current_rig_target = 0
current_rigs = []
all_rigs = []
reserve_rigs = []
rig_no = 0
wells_left = True

## Just go through all the days and wells off the line as rigs become available

for day in range(final_day):

    if not wells_left:
        break

    ## Set the current rig target based on the highest day attained
    for event in rig_list:
        if day >= float(event[0]):
            current_rig_target = float(event[1])

    ## Check if there are enough rigs in current rigs, if not pick up as many as necessary
    if len(current_rigs) < current_rig_target:
        while len(current_rigs) < current_rig_target:
            if len(reserve_rigs) > 0:
                new_rig = reserve_rigs.pop(-1)
            else:
                rig_no += 1
                new_rig = rig(rig_no)
                all_rigs.append(new_rig)
            current_rigs.append(new_rig)

    if len(current_rigs) > current_rig_target:
        while len(current_rigs) > current_rig_target:
            reserve_rigs.append(current_rigs.pop(-1))  ## pop off the last rig on the reserve list


    ## Check all the rigs for an opening in their schedule
    for my_rig in current_rigs:
        if my_rig.days_left == 0:
            my_rig.occupied = False

        if not my_rig.occupied:
            if len(well_list) > 0:
                new_well = well_list.pop(0)
                my_rig.wells_drilled.append(new_well)
                my_rig.days_left = int(new_well[1])
                my_rig.occupied = True
            else:
                wells_left = False

        my_rig.days_left = my_rig.days_left - 1

final_list = []
for rig in all_rigs:
    total_time = 0
    for well in rig.wells_drilled:
        final_list.append([rig.name] + [well[-1]] + [total_time])
        total_time += float(well[1])

f = open('RigSchedule.txt','w')
for line in final_list:
    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
    wr.writerow(line)
