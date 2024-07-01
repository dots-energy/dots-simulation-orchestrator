<?xml version='1.0' encoding='UTF-8'?>
<esdl:EnergySystem xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:esdl="http://www.tno.nl/esdl" version="1" id="37e0284d-29f8-453e-91ec-2e7e02b5c16d" name="EnergySystem" description="Small energy system with assets used in GO-e" esdlVersion="v2211">
  <energySystemInformation xsi:type="esdl:EnergySystemInformation" id="8c79e632-1d89-4198-b055-157856e6fc9f">
    <carriers xsi:type="esdl:Carriers" id="02fafa20-a1bd-488e-a4db-f3c0ca7ff51a">
      <carrier xsi:type="esdl:ElectricityCommodity" id="d88696c0-b536-466b-adbf-429f282afeab" name="Electricity"/>
    </carriers>
  </energySystemInformation>
  <instance xsi:type="esdl:Instance" id="7972c9af-a7c9-4b06-9538-070cfa25291b" name="instance">
    <area xsi:type="esdl:Area" id="757e25b5-908f-4934-a16d-880c63c84406" name="area_title">
      <asset xsi:type="esdl:Bus" name="bus" id="44530afd-832b-4acf-998d-5654359ed813" voltage="400.0">
        <geometry xsi:type="esdl:Point" lat="51.444378637449404" lon="5.326824188232422"/>
        <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="4c9141e6-4df1-4ed6-97c4-4a7146034ff8" id="bdae0341-c510-4bc6-a6f8-2a564f7a5bf3"/>
        <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="a663919d-43e7-4cd5-8e04-01ed1fd8f7d5" id="072ad846-fa1f-43f5-a67d-a16df3f88d21"/>
        <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="2978ba34-820e-45dc-bdc8-530ed856c33e" id="ada56a6a-80b2-4542-bb6e-2a475c3a4ac6"/>
        <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="23c115d9-655d-4249-abb9-4643de97aee3" id="5f139a1a-4415-44a1-866e-9da3eb112485"/>
        <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="6fcd6063-0b4f-42b7-b1f2-5a4fcbaf7ec8" id="a98ca5f6-3aec-412a-bc69-a9ca02c63181"/>
      </asset>
      <asset xsi:type="esdl:Building" name="house0" id="b2a523ae-cb89-44dd-b41f-9fd47aba5c0d">
        <geometry xsi:type="esdl:Point" lat="51.44473304736181" lon="5.327843427658082"/>
        <asset xsi:type="esdl:EConnection" name="connection0" id="e1b3dc89-cee8-4f8e-81ce-a0cb6726c17e">
          <geometry xsi:type="esdl:Point" lat="260.0" lon="52.0" CRS="Simple"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="bdae0341-c510-4bc6-a6f8-2a564f7a5bf3" id="4c9141e6-4df1-4ed6-97c4-4a7146034ff8"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="71a80838-4e6d-4ae2-8358-bd7c2a12386b" id="983c61ea-d305-474a-bada-5886dd49c6f8"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation0" id="1830a516-fae5-4cc7-99bd-6e9a5d175a80" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="415.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="983c61ea-d305-474a-bada-5886dd49c6f8" id="71a80838-4e6d-4ae2-8358-bd7c2a12386b"/>
        </asset>
      </asset>
      <asset xsi:type="esdl:Building" name="house1" id="00ab1742-0480-4a1d-a668-d09f5bca9e2f">
        <geometry xsi:type="esdl:Point" lat="51.44436826693578" lon="5.327478647232056"/>
        <asset xsi:type="esdl:EConnection" name="connection1" id="f006d594-0743-4de5-a589-a6c2350898da">
          <geometry xsi:type="esdl:Point" lat="260.0" lon="52.0" CRS="Simple"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="072ad846-fa1f-43f5-a67d-a16df3f88d21" id="a663919d-43e7-4cd5-8e04-01ed1fd8f7d5"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="296f937e-2e89-4be9-9d70-86f98a3de9ec" id="711a37c7-604c-4906-8e61-cec2b2c8e3bb"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="85b715d0-9851-40a4-a432-969245779b2f" id="33d0e20e-f618-4133-8eab-aa1bbb57e2ea"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation1" id="176af591-6d9d-4751-bb0f-fac7e99b1c3d" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="415.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="711a37c7-604c-4906-8e61-cec2b2c8e3bb" id="296f937e-2e89-4be9-9d70-86f98a3de9ec"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation1" id="b8766109-5328-416f-9991-e81a5cada8a6" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="365.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="33d0e20e-f618-4133-8eab-aa1bbb57e2ea" id="85b715d0-9851-40a4-a432-969245779b2f"/>
        </asset>
      </asset>
      <asset xsi:type="esdl:Building" name="house2" id="9a6f92f2-69db-4435-9730-e37d9f1f61ba">
        <geometry xsi:type="esdl:Point" lat="51.44400348650976" lon="5.327113866806029"/>
        <asset xsi:type="esdl:EConnection" name="connection2" id="f3857348-cbd8-4a89-9e37-cbcf67e649d7">
          <geometry xsi:type="esdl:Point" lat="260.0" lon="52.0" CRS="Simple"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="ada56a6a-80b2-4542-bb6e-2a475c3a4ac6" id="2978ba34-820e-45dc-bdc8-530ed856c33e"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="a966c1c9-2abf-407c-b8e7-8784ab8c77ba" id="cdb6700a-a730-4409-9830-70a61bc4781c"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="288403a8-25fc-4bf9-a975-6592ab84e12b" id="92627339-be9c-4467-afe8-7e0ac2ab04ed"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="fdd2f313-34fc-4919-a6d2-8a9df7997ae5" id="bc345447-59bb-4fe3-9b35-d88cc56c1b7c"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation2" id="529aca74-b8da-4489-9d76-1b2320aa3f40" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="415.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="cdb6700a-a730-4409-9830-70a61bc4781c" id="a966c1c9-2abf-407c-b8e7-8784ab8c77ba"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation2" id="2113dfc3-08d4-40df-8e76-9e53a55d3342" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="365.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="92627339-be9c-4467-afe8-7e0ac2ab04ed" id="288403a8-25fc-4bf9-a975-6592ab84e12b"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation2" id="fdfd4af3-570b-4b81-ac5f-46ca1e687764" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="315.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="bc345447-59bb-4fe3-9b35-d88cc56c1b7c" id="fdd2f313-34fc-4919-a6d2-8a9df7997ae5"/>
        </asset>
      </asset>
      <asset xsi:type="esdl:Building" name="house3" id="d7a38cbc-8eff-4da0-9210-e3937b356645">
        <geometry xsi:type="esdl:Point" lat="51.44363870608373" lon="5.326749086380003"/>
        <asset xsi:type="esdl:EConnection" name="connection3" id="e8711505-2744-48e9-b863-b7bd58722d3b">
          <geometry xsi:type="esdl:Point" lat="260.0" lon="52.0" CRS="Simple"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="5f139a1a-4415-44a1-866e-9da3eb112485" id="23c115d9-655d-4249-abb9-4643de97aee3"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="5d66726a-90b1-4b16-b178-0b4bc21b8e3a" id="f996c994-d7fb-495d-a245-b08c8a42b416"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="df238b43-e9fb-4f59-b1e0-bb8e981b24c9" id="3a51586f-4c22-4fc1-ba2b-20628b96d36d"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="2c9ccc8f-7e7b-4c5a-a576-1076f1c075be" id="9260f24e-457d-4374-b08b-16d40a0344ef"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="88da31ff-df5a-48bd-8596-49ac40596943" id="7ab27e01-7f25-438c-84cd-9ac9408097aa"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation3" id="2d81c891-40e7-46c4-bedc-44421085a7a6" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="415.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="f996c994-d7fb-495d-a245-b08c8a42b416" id="5d66726a-90b1-4b16-b178-0b4bc21b8e3a"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation3" id="d6ccc94f-876c-4c6a-9917-8a3fa6975dc2" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="365.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="3a51586f-4c22-4fc1-ba2b-20628b96d36d" id="df238b43-e9fb-4f59-b1e0-bb8e981b24c9"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation3" id="0f2fc1a6-db36-40a4-932f-31d4fddeac42" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="315.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="9260f24e-457d-4374-b08b-16d40a0344ef" id="2c9ccc8f-7e7b-4c5a-a576-1076f1c075be"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation3" id="4ba625a0-78bd-495a-83cd-726f52befcd7" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="265.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="7ab27e01-7f25-438c-84cd-9ac9408097aa" id="88da31ff-df5a-48bd-8596-49ac40596943"/>
        </asset>
      </asset>
      <asset xsi:type="esdl:Building" name="house4" id="0269b285-c826-43fc-be0a-312a3baca12a">
        <geometry xsi:type="esdl:Point" lat="51.44327392565771" lon="5.326384305953977"/>
        <asset xsi:type="esdl:EConnection" name="connection4" id="51dd7fc3-323f-4262-b7ef-64c38ba59f8f">
          <geometry xsi:type="esdl:Point" lat="260.0" lon="52.0" CRS="Simple"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="a98ca5f6-3aec-412a-bc69-a9ca02c63181" id="6fcd6063-0b4f-42b7-b1f2-5a4fcbaf7ec8"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="b1319be4-0ac0-4107-8782-fd6f9b9bb8e4" id="9df13e84-1f73-4ff5-b085-042f135cf124"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="5a8b83a0-418b-41ba-b938-f3fc4ce04bba" id="0ea8d110-a027-49e3-936a-d6c5a30c2cf4"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="49fc9a88-2910-4ab8-8df5-4b85eefd108a" id="6106cdce-8366-4310-8cbb-5e37de41cb40"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="d20f94cf-9e71-4d09-a506-b49dc30ead71" id="06546308-ac87-48f6-956b-a6983614e293"/>
          <port xsi:type="esdl:InPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="2decec33-402e-48df-a56c-ac7dd0c05b67" id="170be1e2-0004-4ae3-bdfd-a9bf7ac6818e"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation4" id="d4af44ac-aab8-40b3-868c-0668bdb1d9f2" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="415.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="9df13e84-1f73-4ff5-b085-042f135cf124" id="b1319be4-0ac0-4107-8782-fd6f9b9bb8e4"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation4" id="6b22f9d6-c184-4ebf-bfd7-804dd2d56f60" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="365.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="0ea8d110-a027-49e3-936a-d6c5a30c2cf4" id="5a8b83a0-418b-41ba-b938-f3fc4ce04bba"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation4" id="afc87f44-b232-462c-9103-01867dee800b" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="315.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="6106cdce-8366-4310-8cbb-5e37de41cb40" id="49fc9a88-2910-4ab8-8df5-4b85eefd108a"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation4" id="10f2b7e1-0da7-4d46-93a5-696cc01ef07e" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="265.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="06546308-ac87-48f6-956b-a6983614e293" id="d20f94cf-9e71-4d09-a506-b49dc30ead71"/>
        </asset>
        <asset xsi:type="esdl:PVInstallation" power="1000.0" name="pv-installation4" id="2ff29e6c-4136-4a12-9dec-85e60d64f990" panelEfficiency="0.2">
          <geometry xsi:type="esdl:Point" lat="215.0" lon="236.0" CRS="Simple"/>
          <port xsi:type="esdl:OutPort" carrier="d88696c0-b536-466b-adbf-429f282afeab" connectedTo="170be1e2-0004-4ae3-bdfd-a9bf7ac6818e" id="2decec33-402e-48df-a56c-ac7dd0c05b67"/>
        </asset>
      </asset>
    </area>
  </instance>
</esdl:EnergySystem>
