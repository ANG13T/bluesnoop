"""
{
    "D5D93B6E-C324-FD7B-F766-63B6F4C84865": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:24",
        "last_seen": "13:05:49"
    },
    "6ADBBD89-CBFF-0FE8-4494-1507AE371766": {
        "name": "S24af6cdfdb3fee9eC",
        "manuf": "Generic/Other",
        "first_seen": "13:05:24",
        "last_seen": "13:05:52"
    },
    "30398AC1-879B-C211-E439-82D1B77C4F33": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:24",
        "last_seen": "13:05:52"
    },
    "896A6A77-088B-2055-E977-B154C7ED0929": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:24",
        "last_seen": "13:05:52"
    },
    "DEC59FD7-5BEF-D9FE-263E-83E340F0B337": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:24",
        "last_seen": "13:05:52"
    },
    "E986D4D4-76E8-B5D2-AD26-6D70037B173B": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:24",
        "last_seen": "13:05:52"
    },
    "1702158D-45D3-A40B-8D06-273A2A3B9408": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:26",
        "last_seen": "13:05:26"
    },
    "A9694FCF-4FF3-DB6C-6537-4144E9A0EBA7": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:26",
        "last_seen": "13:05:26"
    },
    "AE2D1C4C-3115-C590-FD6D-4CCCC4C8604D": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:31",
        "last_seen": "13:05:44"
    },
    "0A658522-F0DA-C58D-70E7-D19D5709314F": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:31",
        "last_seen": "13:05:31"
    },
    "11FEF887-58B0-3E9A-EFC8-79286AF325FF": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:34",
        "last_seen": "13:05:34"
    },
    "3BF6E0A2-518D-D14C-C174-36BAD878BD75": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:34",
        "last_seen": "13:05:34"
    },
    "65BBE755-C06F-4CE8-B59E-899324B76D44": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:34",
        "last_seen": "13:05:34"
    },
    "BDD92818-08B6-9AB3-44E9-DB58D1323EDD": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:42",
        "last_seen": "13:05:42"
    },
    "4C6450DE-434F-59DA-7C28-1642D43F471D": {
        "name": "Unknown",
        "manuf": "Generic/Other",
        "first_seen": "13:05:44",
        "last_seen": "13:05:44"
    }
}
"""

from OuiLookup import OuiLookup

def uuid_testing(name):
    OuiLookup().query(name)


if __name__ == "__main__":
    test_uuids = [
        "D5D93B6E-C324-FD7B-F766-63B6F4C84865",
        "6ADBBD89-CBFF-0FE8-4494-1507AE371766",
        "30398AC1-879B-C211-E439-82D1B77C4F33",
        "896A6A77-088B-2055-E977-B154C7ED0929",
        "DEC59FD7-5BEF-D9FE-263E-83E340F0B337",
        "E986D4D4-76E8-B5D2-AD26-6D70037B173B",
        "1702158D-45D3-A40B-8D06-273A2A3B9408",
        "A9694FCF-4FF3-DB6C-6537-4144E9A0EBA7",
        "AE2D1C4C-3115-C590-FD6D-4CCCC4C8604D",
        "0A658522-F0DA-C58D-70E7-D19D5709314F",
        "11FEF887-58B0-3E9A-EFC8-79286AF325FF",
        "3BF6E0A2-518D-D14C-C174-36BAD878BD75",
        "65BBE755-C06F-4CE8-B59E-899324B76D44",
        "BDD92818-08B6-9AB3-44E9-DB58D1323EDD"
    ]

    for test_uuid in test_uuids:
        uuid_testing(test_uuid)