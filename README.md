Telnyx Challenge to assign requests to an available VLan on a Device

    Developed with Python-3.8

    1. Install python requirements
        
        $ pip3 install -r requirements.txt
        
    2. Run script
        
        # Inputs (data/requests.csv, data/vlans.csv)
        # Output (data/output.csv)
        
        $ python3 telnyx_script.py 
        
    3. Run script as test mode
    
        # Inputs (data/test_requests.csv, data/test_vlans.csv)
        # Output (data/test_output.csv)
        
        $ python3 telnyx_script.py --env="test"
        
    4. Run Unit test
    
        $ python3 unit_test.py