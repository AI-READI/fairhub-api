from __main__ import app


from faker import Faker


@app.route("/participants", methods=["GET"])
def get_participants():
    fake = Faker()
    data = [
        {
            "participant_id": _ + 1,
            "name": fake.name(),
            "address": fake.street_address(),
            "age": fake.random_int(min=1, max=99),
        }
        for _ in range(30)
    ]

    return data
