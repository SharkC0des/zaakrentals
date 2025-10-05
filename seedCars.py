from app import app
from database import db
from objects import Car

with app.app_context():
    db.create_all()

    if Car.query.count() == 0:

        car1 = Car(
        model="Porsche Sports Car",
        price=69,
        details="High-performance luxury, stunning speed and handling.",
        image="https://file.kelleybluebookimages.com/kbb/base/evox/CP/51956/2023-Porsche-911-front_51956_032_2400x1800_0Q.png",
        vehicle_type="Sedan",
        passengers=2,
        doors=2,
        location="NY"
        )

        car2 = Car(
            model="BMW Sedan 4 Door",
            price=110,
            details="Executive comfort, smooth ride, and sophisticated styling.",
            image="https://images.dealer.com/ddc/vehicles/2024/BMW/M3/Sedan/perspective/front-left/2024_76.png",
            vehicle_type="Sedan",
            passengers=4,
            doors=4,
            location="NY"
        )

        car3 = Car(
            model="Tesla SUV 4 Door",
            price=67,
            details="Electric efficiency, spacious interior, and cutting-edge tech.",
            image="https://file.kelleybluebookimages.com/kbb/base/evox/CP/14481/2020-Tesla-Model%20Y-front_14481_032_2400x1800_PPSW.png",
            vehicle_type="SUV",
            passengers=5,
            doors=4,
            location="NY"
        )

        AdamsCar = Car(
            model="Mitsubishi Outlander 2014",
            price=80085,
            details="Kinda a beater but it got adam through highschool so its chill",
            image="https://img2.carmax.com/assets/mmy-mitsubishi-outlander-2014/image/1.jpg?width=800&height=600",
            vehicle_type="SUV",
            passengers=5,
            doors=4,
            location="ME"
        )

        ZachsCar = Car(
            model="2006 Toyota Matrix",
            price=1,
            details="Top speed of 75 and a turn radius of a train",
            image="https://crdms.images.consumerreports.org/c_lfill,w_563,q_auto,f_auto/prod/cars/chrome-historical/white/USB60TOC172B0101",
            vehicle_type="SUV",
            passengers=5,
            doors=4,
            location="RI"
        )

        JeepWrangler = Car(
            model="Jeep Wrangler 4 dr",
            price=92,
            details="Rugged 4x4, perfect for off-road adventure with removable top.",
            image="https://vexstockimages.fastly.carvana.io/stockimages/2021_JEEP_WRANGLER%20UNLIMITED%204XE_HIGH%20ALTITUDE%204XE%20SPORT%20UTILITY%204D_WHITE_stock_desktop_1920x1080.png?v=1679945137.768",
            vehicle_type="SUV",
            passengers=5,
            doors=4,
            location="RI"
        )

        db.session.add(car1)
        db.session.add(car2)
        db.session.add(car3)
        db.session.add(AdamsCar)
        db.session.add(JeepWrangler)
        db.session.add(ZachsCar)

        db.session.commit()

        print("Seeded Cars success")
    else :
        print(f"Database already has {Car.query.count()} cars. Skipping seed.")

        

    
   # db.session.add(car4)


    


