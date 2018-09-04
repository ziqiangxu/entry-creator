import dbus
bus = dbus.SystemBus()
proxy = bus.get_object('org.freedesktop.PolicyKit1', '/org/freedesktop/PolicyKit1/Authority')
authority = dbus.Interface(proxy, dbus_interface='org.freedesktop.PolicyKit1.Authority')

system_bus_name = bus.get_unique_name()

subject = ('system-bus-name', {'name' : system_bus_name})
action_id = 'org.yixiu.p-test'
details = {}
flags = 1            # AllowUserInteraction flag
cancellation_id = '' # No cancellation id

result = authority.CheckAuthorization(subject, action_id, details, flags, cancellation_id)

print(result)