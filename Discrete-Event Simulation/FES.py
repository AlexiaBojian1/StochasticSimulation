import heapq
from collections import deque
import random
import math



class Event:
    ARRIVAL = 0
    DEPARTURE = 1

    def __init__(self, etype, time, customer=None):
        self.type = etype
        self.time = time
        self.customer = customer

    def __lt__(self, other):
        """For heapq to sort events by their event time."""
        return self.time < other.time

    def __repr__(self):
        """String representation (useful for debugging)."""
        if self.type == Event.ARRIVAL:
            return f"ARRIVAL@{self.time:.4f}"
        else:
            return f"DEPARTURE@{self.time:.4f}"


class FES:
    """Future Event Set implemented with a min-heap."""

    def __init__(self):
        self.heap = []  # min-heap of events

    def add(self, event):
        heapq.heappush(self.heap, event)

    def next(self):
        """Pop the event with the smallest event time."""
        if self.heap:
            return heapq.heappop(self.heap)
        return None

    def peek(self):
        """Return (without removing) the earliest event, or None if empty."""
        if self.heap:
            return self.heap[0]
        return None

    def __len__(self):
        return len(self.heap)

    def updateEventTimes(self, current_time, oldQL, newQL):
        """
        For processor-sharing: 
        - If the queue length changes from oldQL to newQL, 
        - we must rescale the *remaining* service times of future departures 
          in the FES. 
        - The factor is (newQL/oldQL) if oldQL>0 and newQL>0.
        """
        # If oldQL == 0 or newQL == 0, or if oldQL==newQL, no scaling needed.
        if oldQL <= 0 or newQL <= 0 or oldQL == newQL:
            return

        scale_factor = float(newQL) / float(oldQL)

        # We'll need to rebuild the heap with updated times
        updated_events = []
        while self.heap:
            evt = heapq.heappop(self.heap)
            # Only DEPARTURE events need to be rescheduled, 
            # because ARRIVAL times do not depend on the queue length.
            if evt.type == Event.DEPARTURE:
                # The fraction of service left depends on how far we are from 'current_time'.
                # The time from now until departure is (evt.time - current_time).
                remaining = evt.time - current_time
                if remaining < 0:
                    # Already should have happened, but just in case
                    remaining = 0.0
                # Rescale the remaining time:
                new_depart_time = current_time + scale_factor * remaining
                evt.time = new_depart_time

            # Put the event (possibly updated) back in a list
            updated_events.append(evt)

        # Push them all back into the heap
        for evt in updated_events:
            heapq.heappush(self.heap, evt)


class Customer:
    """Simple class to store arrival time and anything else needed."""
    def __init__(self, arrival_time):
        self.arrivalTime = arrival_time

class SimResults:
    """
    Tracks queue length over time and sojourn times (waiting + service).
    """
    def __init__(self):
        self.oldTime = 0.0
        self.sumQL = 0.0
        self.countQL = 0
        self.queueLengthsHistory = []  # optional, store (time, ql)
        self.sojournTimes = []

    def registerQueueLength(self, now, ql):
        """Accumulate area under the curve for Q(t)."""
        # If we want to do time-weighted average, we need the difference from oldTime to now:
        dt = now - self.oldTime
        if dt < 0:
            dt = 0
        self.sumQL += ql * dt
        self.oldTime = now
        self.queueLengthsHistory.append((now, ql))

    def registerSojournTime(self, soj):
        """Record a completed customer's sojourn time."""
        self.sojournTimes.append(soj)

    def getMeanQueueLength(self):
        if not self.queueLengthsHistory:
            return 0.0
        # total time spanned
        last_t = self.queueLengthsHistory[-1][0]  # time of last update
        if last_t == 0:
            return 0.0
        return self.sumQL / last_t

    def getMeanSojournTime(self):
        if len(self.sojournTimes) == 0:
            return 0.0
        return sum(self.sojournTimes) / len(self.sojournTimes)

    def __str__(self):
        return (f"Avg Queue Length = {self.getMeanQueueLength():.4f}, "
                f"Avg Sojourn Time = {self.getMeanSojournTime():.4f}")

class ProcessorSharingSimulation:
    def __init__(self, arrDist, servDist):
        """
        arrDist: function or object with .rvs() -> arrival increments
        servDist: function or object with .rvs() -> base service time
        """
        self.arrDist = arrDist
        self.servDist = servDist

    def simulate(self, T):
        fes = FES()              # Future Event Set
        res = SimResults()       # Collect results
        queue = deque()          # The queue (list of customers)
        t = 0.0                  # current simulation time

        # 1) Schedule first arrival
        first_cust = Customer(self.arrDist.rvs())  
        first_event = Event(Event.ARRIVAL, first_cust.arrivalTime, first_cust)
        fes.add(first_event)

        # 2) Main loop
        while t < T:
            e = fes.next()
            if e is None:
                # No more events; we can stop
                break
            t = e.time  # jump clock to event time
            c1 = e.customer
            oldQL = len(queue)
            # Record queue length at this event
            res.registerQueueLength(t, oldQL)

            if e.type == Event.ARRIVAL:
                # Add customer to queue
                queue.append(c1)

                # IMPORTANT: update departure events because Q length changed: oldQL -> oldQL+1
                fes.updateEventTimes(t, oldQL, oldQL + 1)

                # Now schedule departure time for this newly arrived customer
                # In processor sharing, if the "base" service is X, 
                # actual time needed is X*(oldQL+1) (since they're sharing).
                base_service = self.servDist.rvs()
                departure_time = t + base_service * (oldQL + 1)
                fes.add(Event(Event.DEPARTURE, departure_time, c1))

                # Also schedule the NEXT arrival
                next_arr_time = t + self.arrDist.rvs()
                next_cust = Customer(next_arr_time)
                fes.add(Event(Event.ARRIVAL, next_arr_time, next_cust))

            elif e.type == Event.DEPARTURE:
                # A customer leaves the system
                res.registerSojournTime(t - c1.arrivalTime)
                # Remove them from the queue
                if c1 in queue:
                    queue.remove(c1)

                # Now fewer customers remain => speed up the others
                fes.updateEventTimes(t, oldQL, oldQL - 1)

        return res

if __name__ == "__main__":
    # Example: M/M/1-PS queue with arrival rate lambda=0.7, service rate mu=0.9
    # We'll use exponential(1/lambda) for arrivals, exponential(1/mu) for service.

    import random

    lambda_val = 0.7
    mu_val = 0.9
    random.seed(12345)  # for reproducible results

    # Make little "distribution" callables
    class ExpArrDist:
        def rvs(self):
            return random.expovariate(lambda_val)
    class ExpServDist:
        def rvs(self):
            return random.expovariate(mu_val)

    arrDist = ExpArrDist()
    servDist = ExpServDist()

    sim = ProcessorSharingSimulation(arrDist, servDist)
    T = 10000.0  # run simulation up to time 10,000
    results = sim.simulate(T)

    print(results)  # prints average queue length & sojourn time
    print("Mean Queue Length =", results.getMeanQueueLength())
    print("Mean Sojourn Time =", results.getMeanSojournTime())

