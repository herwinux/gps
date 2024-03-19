from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from plyer import gps
from kivy.utils import platform
from android.permissions import request_permissions, Permission

class GPSApp(App):
    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a callback.
        The request will produce a popup if permissions have not already been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(_, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            if all([res for res in results]):
                # Inicia el sensor GPS
                gps.configure(on_location=self.on_location)
                gps.start()
                #self.on_location()
                #gps.start(1000, 0)
                #self.gps_status = "Callback. All permissions granted."
            else:
                self.gps_status = "Callback. Some permissions refused."

        request_permissions([Permission.ACCESS_COARSE_LOCATION,Permission.ACCESS_FINE_LOCATION, Permission.ACCESS_BACKGROUND_LOCATION], callback)

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.latitude_label = Label(text="Latitud: ")
        self.longitude_label = Label(text="Longitud: ")
        self.layout.add_widget(self.latitude_label)
        self.layout.add_widget(self.longitude_label)
        # Iniciamos la actualización de la ubicación
        #gps.configure(on_location=self.on_location, on_status=self.on_status)
        #gps.start()

        # Actualizamos la ubicación cada segundo
        self.request_android_permissions()

        Clock.schedule_interval(self.update_location, 3)
        return self.layout

    def on_location(self, **kwargs):
        self.latitude_label.text = "Latitud: {}".format(kwargs['lat'])
        self.longitude_label.text = "Longitud: {}".format(kwargs['lon'])


    def on_status(self, stype, status):
        if stype == 'error':
            print('GPSp error: ', status)

    def update_location(self, dt):
        gps.start()

if __name__ == '__main__':
    GPSApp().run()
