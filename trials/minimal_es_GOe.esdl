<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" name="EnergySystem" id="1220aa06-a91c-4386-bb24-1e76e4d52a38" description="Scripted version of first_ESDL_GOe">
  <instance xsi:type="esdl:Instance" id="eb61c8ec-cb25-4175-a184-3d9d1eb5a7d8" name="instance">
    <area xsi:type="esdl:Area" id="7010f2f2-f73d-4c2f-8f09-94c69999f4f0" name="area_title">
      <asset xsi:type="esdl:ElectricityNetwork" id="3d144141-c75b-49d4-81bf-e7a0a3edba67" voltage="230.0" name="network">
        <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="2da1c1e6-0479-4e23-8cfd-3e978484472a" connectedTo="75379e8d-3c96-4391-9300-2ee10b61c5ad"/>
        <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="bb1e5695-2b3f-4efe-b25e-7a1ca001dfcf" connectedTo="33e30f8b-1ef8-4632-bc95-e47a2fe2d387"/>
        <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="f70cf8a7-7eb7-4e32-92f0-e4d9f90d1b24" connectedTo="132731c2-8d47-4cd8-a9b2-79214896e620"/>
        <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="60bc0ef9-4a99-4191-a06c-54442e139d6a" connectedTo="565cfff6-3936-4778-bb8e-bbfc5ef9f5e8"/>
        <geometry xsi:type="esdl:Point" lon="5.326824188232422" lat="51.444378637449404"/>
      </asset>
      <asset xsi:type="esdl:Building" id="c74e3335-2237-4a05-b45f-c254ba1a1616" name="house0">
        <asset xsi:type="esdl:EConnection" id="c3c947f6-ea00-48c7-97c7-16e91aa1d4d3" name="connection0">
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="75379e8d-3c96-4391-9300-2ee10b61c5ad" connectedTo="2da1c1e6-0479-4e23-8cfd-3e978484472a"/>
          <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="6f8347aa-92bd-4b3a-9f35-2d8b7ddd10d5" connectedTo="5571ccab-6ce6-4e7b-a82b-1d259809c0ca"/>
          <geometry xsi:type="esdl:Point" lon="52.0" CRS="Simple" lat="260.0"/>
        </asset>
        <asset xsi:type="esdl:ElectricityNetwork" id="e4d2ab7e-c711-4a44-b3f7-5dab794a093c" name="grid_house0">
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="5571ccab-6ce6-4e7b-a82b-1d259809c0ca" connectedTo="6f8347aa-92bd-4b3a-9f35-2d8b7ddd10d5"/>
          <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="7b4c0f8b-c197-4ccf-8334-46874714b0d6" connectedTo="bb1370bf-d0f6-43e2-a8c2-f11deac1771d"/>
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="c025f577-3dab-4a90-b1f8-f671ea3865a4" connectedTo="7b61ae69-d183-4868-a7fe-7967c163d394"/>
          <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="2fe6469a-80de-48b7-95fd-bef86fcf2f1a" connectedTo="ff2bbb20-7dc7-4073-8813-c8168d6744af"/>
          <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="172bdb5f-9d23-4a13-917a-740284ca44bc" connectedTo="a31a5bf1-1d00-45d1-a34d-dbef8f6cf283"/>
          <geometry xsi:type="esdl:Point" lon="236.0" lat="260.0"/>
        </asset>
        <asset xsi:type="esdl:ElectricityDemand" id="d3ac3422-2418-4506-8003-fb8ea4b95152" name="demand_house0">
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="bb1370bf-d0f6-43e2-a8c2-f11deac1771d" connectedTo="7b4c0f8b-c197-4ccf-8334-46874714b0d6"/>
          <geometry xsi:type="esdl:Point" lon="445.0" CRS="Simple" lat="260.0"/>
        </asset>
        <asset xsi:type="esdl:PVPanel" id="7e663e69-ac06-43ea-a4bb-1b3998e9923c" panelEfficiency="0.2" power="1000.0" name="pv-panel0">
          <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="7b61ae69-d183-4868-a7fe-7967c163d394" connectedTo="c025f577-3dab-4a90-b1f8-f671ea3865a4"/>
          <geometry xsi:type="esdl:Point" lon="236.0" CRS="Simple" lat="415.0"/>
        </asset>
        <asset xsi:type="esdl:EVChargingStation" id="ead7147c-17b4-4d22-9f14-613d8da8aac5" name="ev_charging_pole0" power="10000.0">
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="ff2bbb20-7dc7-4073-8813-c8168d6744af" connectedTo="2fe6469a-80de-48b7-95fd-bef86fcf2f1a"/>
          <geometry xsi:type="esdl:Point" lon="296.0" CRS="Simple" lat="105.0"/>
        </asset>
        <asset xsi:type="esdl:Battery" id="06db0b1e-8359-4a6e-86cb-0232b925ec52" chargeEfficiency="0.98" name="battery" maxDischargeRate="5000.0" maxChargeRate="5000.0" dischargeEfficiency="0.98" fillLevel="50.0" capacity="36000000.0">
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="a31a5bf1-1d00-45d1-a34d-dbef8f6cf283" connectedTo="172bdb5f-9d23-4a13-917a-740284ca44bc"/>
          <geometry xsi:type="esdl:Point" lon="176.0" CRS="Simple" lat="105.0"/>
        </asset>
        <geometry xsi:type="esdl:Point" lon="5.327843427658082" lat="51.44473304736181"/>
      </asset>
      <asset xsi:type="esdl:Building" id="f26758f0-22ba-40b0-ae91-c3785541308e" name="house1">
        <asset xsi:type="esdl:EConnection" id="56178e38-0a00-410d-884b-b8a05c986f0b" name="connection1">
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="33e30f8b-1ef8-4632-bc95-e47a2fe2d387" connectedTo="bb1e5695-2b3f-4efe-b25e-7a1ca001dfcf"/>
          <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="94e67ee5-8779-447e-8943-1c4023c73158" connectedTo="604d52df-14f3-498a-b5c0-e3dfe5549382"/>
          <geometry xsi:type="esdl:Point" lon="52.0" CRS="Simple" lat="260.0"/>
        </asset>
        <asset xsi:type="esdl:ElectricityNetwork" id="a9f8a26e-7296-43fa-8b2f-71fea8cc2696" name="grid_house1">
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="604d52df-14f3-498a-b5c0-e3dfe5549382" connectedTo="94e67ee5-8779-447e-8943-1c4023c73158"/>
          <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="c4fda7a4-21c9-4d8c-8baf-f79afc882b70" connectedTo="0abb05cc-ccd6-4ae8-9556-a9f0bbc7d909"/>
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="5e504be9-2974-4f2c-b0a4-0dc82ba3cf64" connectedTo="3dbf3a9c-bb7c-47d8-b0b0-c85e9f3c5e38"/>
          <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="dca1ba4e-d575-4113-82b2-3f2d7c5801db" connectedTo="42acfa6b-6c2c-41c6-96e8-fed2123a83a4"/>
          <geometry xsi:type="esdl:Point" lon="236.0" lat="260.0"/>
        </asset>
        <asset xsi:type="esdl:ElectricityDemand" id="dbce5fc5-0769-4d69-a95b-934e97cdcb18" name="demand_house1">
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="0abb05cc-ccd6-4ae8-9556-a9f0bbc7d909" connectedTo="c4fda7a4-21c9-4d8c-8baf-f79afc882b70"/>
          <geometry xsi:type="esdl:Point" lon="445.0" CRS="Simple" lat="260.0"/>
        </asset>
        <asset xsi:type="esdl:PVPanel" id="1e05319c-22bc-42c7-9697-9e80206eb884" panelEfficiency="0.2" power="1000.0" name="pv-panel1">
          <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="3dbf3a9c-bb7c-47d8-b0b0-c85e9f3c5e38" connectedTo="5e504be9-2974-4f2c-b0a4-0dc82ba3cf64"/>
          <geometry xsi:type="esdl:Point" lon="236.0" CRS="Simple" lat="415.0"/>
        </asset>
        <asset xsi:type="esdl:HeatPump" id="6d2aff0f-6090-4d3e-a852-7dd5eb421bf2" name="battery" COP="3.0" power="4000.0">
          <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="42acfa6b-6c2c-41c6-96e8-fed2123a83a4" connectedTo="dca1ba4e-d575-4113-82b2-3f2d7c5801db"/>
          <port xsi:type="esdl:OutPort" carrier="9fb67a12-f19b-494b-b1a8-25d255eb94ea" id="91d8640f-477a-4451-8251-5bc7db0e909d" connectedTo="4670ad2d-fdd2-4106-bd8c-ee694be853e5"/>
          <geometry xsi:type="esdl:Point" lon="296.0" CRS="Simple" lat="105.0"/>
        </asset>
        <asset xsi:type="esdl:HeatingDemand" id="3da9f189-0875-441e-b8aa-87b648843274" name="heat_demand">
          <port xsi:type="esdl:InPort" carrier="9fb67a12-f19b-494b-b1a8-25d255eb94ea" id="4670ad2d-fdd2-4106-bd8c-ee694be853e5" connectedTo="91d8640f-477a-4451-8251-5bc7db0e909d"/>
          <geometry xsi:type="esdl:Point" lon="176.0" CRS="Simple" lat="105.0"/>
        </asset>
        <geometry xsi:type="esdl:Point" lon="5.327478647232056" lat="51.44495705975564"/>
      </asset>
      <asset xsi:type="esdl:Import" id="85760eed-0c9c-4092-8dd1-ee0ab822954f" power="1000000.0" name="import" prodType="FOSSIL">
        <port xsi:type="esdl:OutPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="132731c2-8d47-4cd8-a9b2-79214896e620" connectedTo="f70cf8a7-7eb7-4e32-92f0-e4d9f90d1b24"/>
        <geometry xsi:type="esdl:Point" lon="5.325547456741334" lat="51.445234566122615"/>
      </asset>
      <asset xsi:type="esdl:EVChargingStation" id="4bebd8bd-3b1b-4520-9d46-e51fbbd91229" name="ev_charging_station" power="10000.0">
        <port xsi:type="esdl:InPort" carrier="fd5ae1ba-9d67-476e-af48-9b13131a1390" id="565cfff6-3936-4778-bb8e-bbfc5ef9f5e8" connectedTo="60bc0ef9-4a99-4191-a06c-54442e139d6a"/>
        <geometry xsi:type="esdl:Point" lon="5.326116085052491" lat="51.44406265041917"/>
      </asset>
    </area>
  </instance>
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="2b597b93-e2f9-4cbf-a827-bcfd871ff33f">
    <carriers xsi:type="esdl:Carriers" id="d260d5a0-c547-4d46-829b-4b248b0d52ea">
      <carrier xsi:type="esdl:ElectricityCommodity" name="Electricity" id="fd5ae1ba-9d67-476e-af48-9b13131a1390"/>
      <carrier xsi:type="esdl:ElectricityCommodity" name="Heat" id="9fb67a12-f19b-494b-b1a8-25d255eb94ea"/>
    </carriers>
  </energySystemInformation>
</esdl:EnergySystem>
