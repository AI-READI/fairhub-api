from flask_restx import fields

REDCapReportStudyDashboardDataModel = {
    "dm": fields.String(
        required=True, readonly=True, description="Data approved for Fairhub.io"
    ),
    "record_id": fields.String(
        required=True, readonly=True, description="Participant record ID"
    ),
    "siteid": fields.String(required=True, readonly=True, description="Site ID"),
    "genderid": fields.String(
        required=True, readonly=True, description="Gender identity"
    ),
    "genderidot": fields.String(
        required=True, readonly=True, description="Gender identity - other"
    ),
    "scrsex": fields.String(required=True, readonly=True, description="Sex at birth"),
    "scrsexot": fields.String(
        required=True, readonly=True, description="Sex at birth - other"
    ),
    "race": fields.String(required=True, readonly=True, description="Race"),
    "raceot": fields.String(required=True, readonly=True, description="Race - other"),
    "race2": fields.String(
        required=True, readonly=True, description="Race further defined"
    ),
    "ethnic": fields.String(required=True, readonly=True, description="Ethnicity"),
    "ethnicot": fields.String(
        required=True, readonly=True, description="Ethnicity - other"
    ),
    "ancestry": fields.String(required=True, readonly=True, description="Ancestry"),
    "recstartts": fields.String(
        required=True,
        readonly=True,
        description="Recruitiment survey started timestamp",
    ),
    "reccmpts": fields.String(
        required=True,
        readonly=True,
        description="Recruitiment survey completed timestamp",
    ),
    "reccmpdat": fields.String(
        required=True, readonly=True, description="Recruitment survey completed date"
    ),
    "faqstartts": fields.String(
        required=True, readonly=True, description="FAQ survey started timestamp"
    ),
    "faqcmpts": fields.String(
        required=True, readonly=True, description="FAQ survey completed timestamp"
    ),
    "faqcmpdat": fields.String(
        required=True, readonly=True, description="FAQ survey completed date"
    ),
    "scrstartts": fields.String(
        required=True, readonly=True, description="Screening survey started timestamp"
    ),
    "scrcmpts": fields.String(
        required=True, readonly=True, description="Screening survey completed timestamp"
    ),
    "scrcmpdat": fields.String(
        required=True, readonly=True, description="Screening survey completed date"
    ),
    "preconstartts": fields.String(
        required=True, readonly=True, description="Pre-consent survey started timestamp"
    ),
    "preconcmpts": fields.String(
        required=True,
        readonly=True,
        description="Pre-consent survey completed timestamp",
    ),
    "preconcmpdat": fields.String(
        required=True, readonly=True, description="Pre-consent survey completed date"
    ),
    "icfsvyts": fields.String(
        required=True, readonly=True, description="Consent survey started timestamp"
    ),
    "icfcmpts": fields.String(
        required=True, readonly=True, description="Consent survey completed timestamp"
    ),
    "icf_dat": fields.String(
        required=True, readonly=True, description="Consent survey completed date"
    ),
    "icfa_dat": fields.String(
        required=True,
        readonly=True,
        description="Staff consent attestation survey completed date",
    ),
    "prtcmpdat": fields.String(
        required=True,
        readonly=True,
        description="Participant contact information survey completed date",
    ),
    "dmgstartts": fields.String(
        required=True,
        readonly=True,
        description="Demographics survey started timestamp",
    ),
    "dmgcmpts": fields.String(
        required=True,
        readonly=True,
        description="Demographics survey completed timestamp",
    ),
    "dmgcmpdat": fields.String(
        required=True, readonly=True, description="Demographics survey completed date"
    ),
    "mhstartts": fields.String(
        required=True, readonly=True, description="Health survey started timestamp"
    ),
    "mhcmpts": fields.String(
        required=True, readonly=True, description="Health survey completed timestamp"
    ),
    "mhcmpdat": fields.String(
        required=True, readonly=True, description="Health survey completed date"
    ),
    "sustartts": fields.String(
        required=True,
        readonly=True,
        description="Substance use survey started timestamp",
    ),
    "sucmpts": fields.String(
        required=True,
        readonly=True,
        description="Substance use survey completed timestamp",
    ),
    "sucmpdat": fields.String(
        required=True, readonly=True, description="Substance use survey completed date"
    ),
    "cesstartts": fields.String(
        required=True, readonly=True, description="CES-D-10 survey started timestamp"
    ),
    "cescmpts": fields.String(
        required=True, readonly=True, description="CES-D-10 survey completed timestamp"
    ),
    "cesmpdat": fields.String(
        required=True, readonly=True, description="CES-D-10 survey completed date"
    ),
    "paidstartts": fields.String(
        required=True, readonly=True, description="PAID-5 DM survey started timestamp"
    ),
    "paidcmpts": fields.String(
        required=True, readonly=True, description="PAID-5 DM survey completed timestamp"
    ),
    "paidcmpdat": fields.String(
        required=True, readonly=True, description="PAID-5 DM survey completed date"
    ),
    "dmlstartts": fields.String(
        required=True, readonly=True, description="Diabetes survey started timestamp"
    ),
    "dmlcmpts": fields.String(
        required=True, readonly=True, description="Diabetes survey completed timestamp"
    ),
    "dmlcmpdat": fields.String(
        required=True, readonly=True, description="Diabetes survey completed date"
    ),
    "dietstartts": fields.String(
        required=True, readonly=True, description="Dietary survey started timestamp"
    ),
    "dietcmpts": fields.String(
        required=True, readonly=True, description="Dietary survey completed timestamp"
    ),
    "dietcmpdat": fields.String(
        required=True, readonly=True, description="Dietary survey completed date"
    ),
    "viastartts": fields.String(
        required=True, readonly=True, description="Opthalmic survey started timestamp"
    ),
    "viacmpts": fields.String(
        required=True, readonly=True, description="Opthalmic survey completed timestamp"
    ),
    "viacmpdat": fields.String(
        required=True, readonly=True, description="Opthalmic survey completed date"
    ),
    "pxsdohstartts": fields.String(
        required=True, readonly=True, description="PhenX SDOH survey started timestamp"
    ),
    "pxsdohcmpts": fields.String(
        required=True,
        readonly=True,
        description="PhenX SDOH survey completed timestamp",
    ),
    "pxsdohcmpdat": fields.String(
        required=True, readonly=True, description="PhenX SDOH survey completed date"
    ),
    "pxfistartts": fields.String(
        required=True,
        readonly=True,
        description="PhenX Food Insecurity survey started timestamp",
    ),
    "pxsficmpts": fields.String(
        required=True,
        readonly=True,
        description="PhenX Food Insecurity survey completed timestamp",
    ),
    "pxsficmpdat": fields.String(
        required=True,
        readonly=True,
        description="PhenX Food Insecurity survey completed date",
    ),
    "pxnestartts": fields.String(
        required=True,
        readonly=True,
        description="PhenX Neighborhood Enviroment survey started timestamp",
    ),
    "pxnecmpts": fields.String(
        required=True,
        readonly=True,
        description="PhenX Neighborhood Enviroment survey completed timestamp",
    ),
    "pxnecmpdat": fields.String(
        required=True,
        readonly=True,
        description="PhenX Neighborhood Enviroment survey completed date",
    ),
    "pxrdcmpts": fields.String(
        required=True,
        readonly=True,
        description="PhenX Racial/Ethnic Discrimination survey started timestamp",
    ),
    "pxrdstartts": fields.String(
        required=True,
        readonly=True,
        description="PhenX Racial/Ethnic Discrimination survey completed timestamp",
    ),
    "pxrdcmpdat": fields.String(
        required=True,
        readonly=True,
        description="PhenX Racial/Ethnic Discrimination survey completed date",
    ),
    "declinestartts": fields.String(
        required=True,
        readonly=True,
        description="Decline Participation survey started timestamp",
    ),
    "declinecmpts": fields.String(
        required=True,
        readonly=True,
        description="Decline Participation survey completed timestamp",
    ),
    "deccmpdat": fields.String(
        required=True,
        readonly=True,
        description="Decline Participation survey completed date",
    ),
    "cnct_sccs": fields.String(
        required=True, readonly=True, description="Contact success"
    ),
    "cnct_type": fields.String(
        required=True, readonly=True, description="Contact type"
    ),
    "cnct_prp": fields.String(
        required=True, readonly=True, description="Contact purpose"
    ),
    "dvenvyn": fields.Boolean(
        required=True, readonly=True, description="Environmental sensor distributed"
    ),
    "dvenvstdat": fields.String(
        required=True,
        readonly=True,
        description="Date of environmental sensor distribution",
    ),
    "dvenvreasn": fields.String(
        required=True,
        readonly=True,
        description="If enviromental sensor not distributed, why?",
    ),
    "dvenvcrcid": fields.String(
        required=True,
        readonly=True,
        description="Was environmental sensor demonstrated?",
    ),
    "dvcgmyn": fields.Boolean(
        required=True, readonly=True, description="Continuous glucose monitor inserted"
    ),
    "dvcgmstdat": fields.String(
        required=True,
        readonly=True,
        description="Date of continuous glucose monitor was inserted",
    ),
    "dvcgmreasn": fields.String(
        required=True,
        readonly=True,
        description="If continuous glucose monitor not inserted, why?",
    ),
    "dvcgmvrfy": fields.Boolean(
        required=True,
        readonly=True,
        description="Continuous glucose monitor initialized and recording?",
    ),
    "dvamwyn": fields.Boolean(
        required=True,
        readonly=True,
        description="Was the Apple watch sent home with the participant?",
    ),
    "dvamwstdat": fields.String(
        required=True,
        readonly=True,
        description="Date Apple watch was given to participant",
    ),
    "dvamwreasn": fields.String(
        required=True,
        readonly=True,
        description="If Apple watch was not given to participant, why?",
    ),
    "dvamwsn": fields.String(
        required=True, readonly=True, description="Apple watch serial number"
    ),
    "dvrtmthd": fields.String(
        required=True, readonly=True, description="Planned method of device return"
    ),
    "dvrtnyn": fields.Boolean(
        required=True,
        readonly=True,
        description="Was the participant given device return instructions and shipping materials?",
    ),
    "dvrtnship": fields.String(
        required=True, readonly=True, description="Return shipping tracking number"
    ),
    "mhterm_dm1": fields.Boolean(
        required=True, readonly=True, description="Type I diabetes"
    ),
    "mhterm_dm2": fields.Boolean(
        required=True, readonly=True, description="Type II diabetes"
    ),
    "mhterm_predm": fields.Boolean(
        required=True, readonly=True, description="Pre-diabetes"
    ),
    "mh_dm_age": fields.String(
        required=True, readonly=True, description="Age diagnosed with type II diabetes"
    ),
    "mh_a1c": fields.Boolean(
        required=True, readonly=True, description="Elevated A1C levels"
    ),
    "cmtrt_a1c": fields.String(
        required=True,
        readonly=True,
        description="Taking pills to control A1C and blood glucose levels?",
    ),
    "cmtrt_insln": fields.Boolean(
        required=True,
        readonly=True,
        description="Injecting insulin to control blood glucose levels",
    ),
    "cmtrt_glcs": fields.Boolean(
        required=True,
        readonly=True,
        description="Using other injectables to control blood glucose levels",
    ),
    "cmtrt_lfst": fields.Boolean(
        required=True,
        readonly=True,
        description="Using lifestyle changes to control blood glucose levels",
    ),
}
