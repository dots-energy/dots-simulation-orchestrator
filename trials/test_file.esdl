<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl"
                   name="EnergySystem" id="1220aa06-a91c-4386-bb24-1e76e4d52a38"
                   description="Scripted version of first_ESDL_GOe">
    <instance xsi:type="esdl:Instance" id="instance_id" name="instance">
        <area xsi:type="esdl:Area" id="area_id" name="area_title">
            <asset xsi:type="esdl:Battery" id="4bebd8bd-3b1b-4520-9d46-e51fbbd91229" chargeEfficiency="0.98"
                   name="battery1" maxDischargeRate="5000.0" maxChargeRate="5000.0" dischargeEfficiency="0.98"
                   fillLevel="50.0" capacity="36000000.0">
                <port xsi:type="esdl:InPort" carrier="carrier_id" id="model_inport1_id"
                      connectedTo="132731c2-8d47-4cd8-a9b2-79214896e620"/>
                <geometry xsi:type="esdl:Point" lon="5.326824188232422" lat="51.444378637449404"/>
            </asset>
            <asset xsi:type="esdl:PVPanel" id="85760eed-0c9c-4092-8dd1-ee0ab822954f" panelEfficiency="0.2"
                   power="1000.0" name="pv-panel1">
                <port xsi:type="esdl:OutPort" carrier="carrier_id"
                      id="132731c2-8d47-4cd8-a9b2-79214896e620" connectedTo="model_inport1_id"/>
                <geometry xsi:type="esdl:Point" lon="5.325547456741334" lat="51.445234566122615"/>
            </asset>

        </area>
    </instance>
    <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="2b597b93-e2f9-4cbf-a827-bcfd871ff33f">
        <carriers xsi:type="esdl:Carriers" id="d260d5a0-c547-4d46-829b-4b248b0d52ea">
            <carrier xsi:type="esdl:ElectricityCommodity" name="Electricity" id="carrier_id"/>
        </carriers>
    </energySystemInformation>
</esdl:EnergySystem>
