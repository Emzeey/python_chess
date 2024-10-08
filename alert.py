class Alerts:
    alert_list = []
    alert_count = 0

    def get_alerts(self):
        return self.alert_list

    def add(self, alert):
        self.alert_count += 1
        self.alert_list.append(alert)

    def get_alert_count(self):
        return self.alert_count

    def print(self):
        if self.alert_count > 0:
            print("Alerts:")
        while self.alert_count > 0:
            print("\t" + self.alert_list.pop(0))
            self.alert_count -= 1
