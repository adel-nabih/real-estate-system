from models.property import Property
from controllers.property_controller import add_property, get_all_properties, assign_broker_to_property
from models.client import Client
from controllers.client_controller import add_client, get_all_clients, assign_broker_to_client
from models.broker import Broker
from controllers.broker_controller import add_broker, get_all_brokers
from models.sale import Sale
from controllers.sale_controller import add_sale, get_all_sales
import datetime

if __name__ == "__main__":
    #p = Property(None, "Zamalek", "Apartment", 150, 4750000, "available")
    #add_property(p)

    # Fetch and print all properties
    #all_props = get_all_properties()
    #or prop in all_props:
     #   print(vars(prop))

     # Add broker before assigning
    # b = Broker(None, "Ahmed Khaled", 5)
    # add_broker(b)

    # # Add a new client
    # c = Client(None, "Sarah Mostafa", "sarah@example.com", "apartment, 2 bedrooms", None)
    # add_client(c)

    # # Assign a broker (assume broker with id 1 exists)
    # assign_broker_to_client(client_id=1, broker_id=1)

    # # Get and print all clients
    # clients = get_all_clients()
    # for client in clients:
    #     print(vars(client))
    # Add a property and assign broker ID 1
    # new_prop = Property(None, "Sheikh Zayed", "Villa", 300, 9500000, "available", broker_id=1)
    # property_id = add_property(new_prop)

    # assign_broker_to_property(property_id, broker_id=1)

    # # Print all properties
    # props = get_all_properties()
    # for p in props:
    #     print(vars(p))

    # # Record a sale
    # sale = Sale(
    #     id=None,
    #     property_id=1,     # make sure this property exists and isn't sold yet
    #     client_id=1,
    #     broker_id=1,
    #     date=datetime.date.today().isoformat(),
    #     final_price=4750000.00
    # )
    # sale_id = add_sale(sale)

    # # Verify sales
    # sales = get_all_sales()
    # for s in sales:
    #     print(vars(s))
    # Add a broker
    b = Broker(None, "Adel Nabih", 8)
    add_broker(b)
    # Fetch and print all brokers
    all_brokers = get_all_brokers()
    for broker in all_brokers:
        print(vars(broker))
    # Add a client
    



