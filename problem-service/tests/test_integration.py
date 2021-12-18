import json, requests, atexit, pytest, os
from pact import Consumer, Like, Provider, Term, Format, Verifier


#initalize pact object be defining the Consumer and Provider objects as well as the pact and log directories
pact = Consumer('Problem Service').has_pact_with(Provider('Image Upload Service'), pact_dir="./pacts", log_dir="./logs")
#Start pact VM
pact.start_service()
#Register observer to notify vm to stop when python exits
atexit.register(pact.stop_service)


def test_get_product():
    #Get the expected response from petstore api
    expected = "eef74ecc-38b9-493f-a854-a65c64846b32"
    body = files=[('image', ('Capture.PNG', open('../Capture.PNG','rb'),'application/octet-stream'))]

    #Create pact file given=Description, uponReceiving=the state the provider is in, Request=Expected Request, Response=The expected response
    (pact.given('the image upload service is available')
    .upon_receiving('a successful insert into the problem db')
    .with_request('POST', '/image/v1/Problem/1', body)
    .will_respond_with(200, body=expected))
    #In the pact context
    with pact:
        #create Petstore consumer object and set endpoint to pact VM (defaults to actual if uri not specified)
        consumer = PetstoreConsumer(uri=pact.uri)
        print(pact.uri)
        #call get pet by id 1
        pet = consumer.get_pet(1)
    verifier = Verifier(provider="Petstore Provider Spring", provider_base_url="http://localhost:8080")
    #pact-verifier --provider-base-url=http://localhost:8080 --pact-url=./pacts/petstore_consumer_python-petstore_provider_spring.json
    output, log = verifier.verify_pacts("./pacts/petstore_consumer_python-petstore_provider_spring.json")
    print(log)
    assert output == 0