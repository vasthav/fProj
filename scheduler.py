import time


class Scheduler:
    unassigned = []
    volunteers = []
    assigned = {}
    timeout = None
    start_time = None
    completed = []

    def __init__(self, list_of_jobs, list_of_volunteers, timeout=None):
        self.unassigned = list_of_jobs
        self.volunteers = list_of_volunteers
        self.timeout = timeout

    def assign(self):
        while (len(self.volunteers) != 0) and (len(self.unassigned) != 0):
            self.assigned[self.unassigned[0]] = self.volunteers[0]
            del self.unassigned[0]
            del self.volunteers[0]
        return self.assigned, self.unassigned

    def set_start_time(self):
        self.start_time = time.time()

    def poll_jobs(self):
        if (time.time() - self.start_time) > self.timeout:
            while (len(self.assigned)) != 0:
                job, volunteer = self.assigned.popitem()
                self.unassigned.append(job)
        return self.unassigned

    def add_to_completed(self, job):
        if job in self.assigned:
            self.completed.append(job)
            del self.assigned[job]


# here job stands for job id
# use dictionary for storing job_id and raw data/results
# requires time module
# use as follows
# create schedule object
# schedule = Scheduler([1, 2, 4, 10, 11], [5, 6, 7, 8], 2)
# set time after sending jobs to peers
# schedule.set_start_time()
# when peer sends back result
# schedule.add_to_completed(4)
# to check at periodic iterations if any jobs have yet to be completed
# print(schedule.poll_jobs())
