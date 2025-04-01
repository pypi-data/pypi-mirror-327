import datetime
import os
from operator import attrgetter

import pytest

from pysll.exceptions import ConstellationObjectDoesNotExistException
from pysll.models import Model, Object, VariableUnitValue


def test_simple_download(client):
    """Test a simple download on a single object."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "Name") == "bsmith"


def test_multiple_objects_download(client):
    """Test a simple download on multiple objects."""
    assert client.download([Object("id:Z1lqpMzvkGMV"), Object("id:o1k9jAGmo6Jm")], "Name") == [
        "bsmith",
        "pavan.shah",
    ]


def test_multiple_field_download(client):
    """Test a simple download on multiple fields."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), ["Name", "FirstName"]) == [
        "bsmith",
        "Ben",
    ]


def test_multiple_field_multiple_object_download(client):
    """Test a simple download multiple objects and fields."""
    assert client.download([Object("id:Z1lqpMzvkGMV"), Object("id:o1k9jAGmo6Jm")], ["Name", "FirstName"]) == [
        ["bsmith", "Ben"],
        ["pavan.shah", "Pavan"],
    ]


def test_download_non_existant_object(client):
    """Test a simple download on a non-existant object."""
    with pytest.raises(ConstellationObjectDoesNotExistException):
        client.download(Object("id:abc123"), "Name")


def test_download_non_existant_field(client):
    """Test a simple download on a non-existant field."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "FakeField") is None


def test_download_empty_field(client):
    """Test a simple download on an empty field."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "Biography") is None


def test_download_empty_link_field(client):
    """Test a simple download on an empty link field."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "ProtocolStack") is None


def test_download_multiple_link_field(client):
    """Test a simple download on a non-existant field."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "FinancingTeams") == [Object("id:1ZA60vLeXa7a")]


def test_download_all(client):
    """Test downloading all fields on an object."""
    all_dict = client.download(Object("id:Z1lqpMzvkGMV"))
    assert all_dict["Name"] == "bsmith"


def test_download_parts(client):
    """Test downloading parts of a field."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "ProtocolsAuthored[[1]]") == Object("id:wqW9BP7dkv8G")


def test_download_parts_traversal(client):
    """Test downloading parts of a field then traversing a link."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "ProtocolsAuthored[[1]][Author]") == Object("id:Z1lqpMzvkGMV")


def test_download_parts_column(client):
    """Test downloading columns of a field."""
    result = client.download(Object("id:o1k9jAKpnRpm"), "Contents[[All,1]]")
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)


def test_download_parts_rows_column(client):
    """Test downloading rows and columns of a field."""
    assert client.download(Object("id:o1k9jAKpnRpm"), "Contents[[1,1]]") == "A1"


def test_download_parts_column_traversal(client):
    """Test downloading via traversal and then fetching columns of a field."""
    result = client.download(Object("id:01G6nvDGrlWE"), "ContainersOut[Contents][[All,1]]")
    assert isinstance(result, list)
    assert len(result) == 4
    assert all(all(isinstance(item, str) for item in subarray) for subarray in result)


def test_download_parts_row_column_traversal(client):
    """Test downloading via traversal and then fetching columns of a field."""
    assert client.download(Object("id:01G6nvDGrlWE"), "ContainersOut[Contents][[1,1]]") == ["A1", "A1", "A1", "A1"]


def test_download_parts_specific_row_column_traversal(client):
    """Test downloading via traversal and then fetching columns of a field."""
    result = client.download(Object("id:01G6nvDGrlWE"), "ContainersOut[[1]][Contents][[All,1]]")
    assert isinstance(result, list)
    assert all(isinstance(item, str) for item in result)


# Downloading Recursively


def test_download_repeated_single_field(client):
    """Test that you can download recursively from a single field."""
    assert client.download(Object("id:4pO6dM57V6K7"), "Repeated[Container]") == [Object("id:xRO9n3BdWrxY")]


def test_download_repeated_single_field_with_traversal(client):
    """Test that you can download recursively from a single field with a
    traversal."""
    assert client.download(Object("id:4pO6dM57V6K7"), "Repeated[Container][Model]") == [Model("id:J8AY5jDwb4B9")]


def test_download_repeated_multiple_field(client):
    """Test that you can download recursively from a multiple field."""
    result = client.download(Object("id:KBL5DvPoNP0a"), "Repeated[Subprotocols]")
    assert isinstance(result, list)
    assert [arr[0] for arr in result[:3]] == [
        Object("id:GmzlKjNBxv7E"),
        Object("id:n0k9mGOWAmXo"),
        Object("id:o1k9jAoWJLk4"),
    ]


def test_download_repeated_multiple_field_with_traversal(client):
    """Test that you can download recursively from a multiple field with a
    traversal."""
    result = client.download(Object("id:KBL5DvPoNP0a"), "Repeated[Subprotocols][DateCreated]")
    assert isinstance(result, list)
    assert [isinstance(item[0], datetime.datetime) for item in result]


def test_download_repeated_buried_traversal(client):
    """Test that you can download recursively from a buried Repeated
    reference."""
    result = client.download(Object("id:4pO6dM5GvK0X"), "Resources[Repeated[Container]][Model]")
    assert isinstance(result, list)
    assert all(len(item) == 1 for item in result)
    assert [isinstance(item[0], Object) for item in result]


def test_download_repeated_multiple_field_with_column(client):
    """Test that you can download recursively from a multiple field that
    required a specific column."""
    result = client.download(Object("id:Z1lqpMz63avW"), "Repeated[Contents[[All,2]]]")
    assert result == [
        [Object("id:o1k9jAGJzXDm"), None],
        [Object("id:GmzlKjPkdpVe"), None],
        [Object("id:8qZ1VW0Mb5OZ"), [[Object("id:M8n3rx0lqXz8"), None], [Object("id:Z1lqpMz63PAo"), None]]],
    ]


def test_download_repeated_multiple_field_with_column_and_traversal(client):
    """Test that you can download recursively from a multiple field that
    required a specific column and then a field traversal."""
    result = client.download(Object("id:Z1lqpMz63avW"), "Repeated[Contents[[All,2]]][Model]")
    assert result == [
        [Model("id:wqW9BP7RBNZG"), None],
        [Model("id:8qZ1VWNw1z0X"), None],
        [Model("id:E8zoYveRll17"), [[Model("id:8qZ1VWNmdLBD"), None], [Model("id:8qZ1VWNmdLBD"), None]]],
    ]


def test_download_repeated_listed_objects(client):
    """Test that you can download from a list of objects with a repeated field
    reference."""
    result = client.download([Object("id:R8e1PjRDvAAK"), Object("id:AEqRl9540rjd")], "Repeated[Subprotocols]")
    assert result[0] == [
        [Object("id:bq9LA0dBD86a"), None],
        [Object("id:n0k9mGzReVYr"), [[Object("id:BYDOjv1VZ0Zr"), None]]],
    ]
    assert result[1] == [
        [Object("id:kEJ9mqaVW6NX"), None],
        [Object("id:jLq9jXY4Bdx1"), [[Object("id:dORYzZn08jnD"), None]]],
    ]


def test_download_repeated_listed_objects_fields(client):
    """Test that you can download from a list of objects with a list of fields
    including a repeated field reference."""
    result = client.download([Object("id:R8e1PjRDvAAK"), Object("id:AEqRl9540rjd")], ["Name", "Repeated[Subprotocols]"])
    assert result[0] == [
        "LegacyID:42",
        [
            [Object("id:bq9LA0dBD86a"), None],
            [Object("id:n0k9mGzReVYr"), [[Object("id:BYDOjv1VZ0Zr"), None]]],
        ],
    ]
    assert result[1] == [
        "LegacyID:43",
        [
            [Object("id:kEJ9mqaVW6NX"), None],
            [Object("id:jLq9jXY4Bdx1"), [[Object("id:dORYzZn08jnD"), None]]],
        ],
    ]


# Downloading links


def test_chained_download(client):
    """Test that you can chain downloads off of links."""
    assert client.download(client.download(Object("id:Z1lqpMzvkGMV"), "FinancingTeams"), "Name") == ["Engineering"]


def test_single_traversal(client):
    """Test that you can traverse links."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "FinancingTeams[Name]") == ["Engineering"]


def test_multiple_traversal(client):
    """Test that you can perform multiple link traversals in a single
    request."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), "FinancingTeams[BillingAddress][Name]") == ["ECL-1"]


def test_multiple_multiple_field(client):
    """Test that you can download a multiple field."""
    field_value = client.download(Object("id:Z1lqpMzvkGMV"), "SafetyTrainingLog")
    assert len(field_value) == 3
    assert field_value[0][1] == "ChemicalHandling"
    assert isinstance(field_value[0][0], datetime.datetime)


def test_multiple_field_single_field_traversal(client):
    """Test that you can download a single field through a multiple field."""
    field_value = client.download(Object("id:Z1lqpMzvkGMV"), "DirectReports[Name]")
    assert field_value == ["tommy.harrelson", "ayi", "brad"]


def test_multiple_field_multiple_field_traversal(client):
    """Test that you can download a multiple field through a multiple field."""
    field_value = client.download(Object("id:Z1lqpMzvkGMV"), "DirectReports[SafetyTrainingLog]")
    assert len(field_value) == 3
    assert field_value[0] is None
    assert len(field_value[1]) == 3
    assert len(field_value[2]) == 3
    assert len(field_value[1][0]) == 3
    assert field_value[1][0][1] == "ChemicalHandling"
    assert isinstance(field_value[1][1][0], datetime.datetime)


# Downloading various types


def test_download_integer(client):
    """Test that integer field types are correctly formatted."""
    assert client.download(Object("id:BYDOjvG4l3Ol"), "InjectionIndex") == 28


def test_download_string(client):
    """Test that string field types are correctly formatted."""
    assert client.download(Object("id:BYDOjvG4l3Ol"), "DataType") == "Analyte"


def test_download_quantity(client):
    """Test that quantity field types are correctly formatted."""
    assert client.download(Object("id:BYDOjvG4l3Ol"), "SampleVolume") == VariableUnitValue(10, "Microliters")


def test_download_date(client):
    """Test that date fields are correctly formatted."""
    # Note - retrieving the default units automatically is not yet supported
    assert client.download(Object("id:BYDOjvG4l3Ol"), "DateInjected") == datetime.datetime(2022, 1, 7, 17, 12, 19)


def test_file_download_with_automatic_download(client):
    """Test that files are automatically downloaded when requested."""
    cloud_file = client.download(Object("id:Z1lqpMzvkGMV"), "PhotoFile", auto_download_cloud_files=True)
    assert os.path.exists(cloud_file.local_path)


def test_file_download_with_automatic_download_and_byte_size(client):
    """Test that files are automatically downloaded when requested."""
    cloud_file = client.download(
        Object("id:Z1lqpMzvkGMV"), "PhotoFile", auto_download_cloud_files=True, byte_size=10_000_000
    )
    assert os.path.exists(cloud_file.local_path)


def test_file_download_without_automatic_download(client):
    """Test that files are not automatically downloaded when not requested."""
    cloud_file = client.download(Object("id:Z1lqpMzvkGMV"), "PhotoFile")
    assert cloud_file == Object("id:KBL5Dvw60ve7")
    assert cloud_file.local_path == ""


def test_blob_ref_download(client):
    """Test that blob refs are downloaded automatically correctly."""
    absorbance_data = client.download(Object("id:BYDOjvG4l3Ol"), "Absorbance")
    assert len(absorbance_data) == 7201
    assert len(absorbance_data[3]) == 2
    assert absorbance_data[3][0].unit == "'Minutes'"
    assert absorbance_data[3][1].unit == "'Milli' 'AbsorbanceUnit'"


def test_absorbance_download(client):
    """Test that Absorbance fields are downloaded automatically correctly.

    Absorbance fields are given by BigQuantityArrays (e.g. blobrefs
    under the hood).
    """
    absorbance_data = client.download(Object("id:9RdZXvdLrJwa"), "Absorbance")
    assert len(absorbance_data) == 2250
    assert len(absorbance_data[3]) == 2
    assert absorbance_data[3][0].unit == "'Minutes'"
    assert absorbance_data[3][1].unit == "'Milli' 'AbsorbanceUnit'"


def test_multi_blob_ref_download(client):
    """Test that multiple blob refs are downloaded automatically correctly."""
    absorbance_data = client.download([Object("id:BYDOjvG4l3Ol"), Object("id:BYDOjvG4l3Ol")], "Absorbance")
    assert len(absorbance_data) == 2
    absorbance_data = absorbance_data[0]
    assert len(absorbance_data) == 7201
    assert len(absorbance_data[3]) == 2
    assert absorbance_data[3][0].unit == "'Minutes'"
    assert absorbance_data[3][1].unit == "'Milli' 'AbsorbanceUnit'"


def test_blob_ref_download_with_byte_size(client):
    """Test that blob refs are downloaded automatically correctly."""
    absorbance_data = client.download(Object("id:BYDOjvG4l3Ol"), "Absorbance", byte_size=10_000_000)
    assert len(absorbance_data) == 7201
    assert len(absorbance_data[3]) == 2
    assert absorbance_data[3][0].unit == "'Minutes'"
    assert absorbance_data[3][1].unit == "'Milli' 'AbsorbanceUnit'"


def test_quantity_array_download(client):
    """Test that quantity arrays are downloaded correctly."""
    scatter_info = client.download(Object("id:BYDOjvG4l3Ol"), "Scattering")
    assert isinstance(scatter_info, list)
    assert len(scatter_info) == 361


def test_variable_unit_download(client):
    """Test that variable units are downloaded correctly."""
    composition = client.download(Object("id:O81aEB16GlJ1"), "Composition")
    assert isinstance(composition, list)
    assert len(composition) == 2
    assert isinstance(composition[0], list)
    assert len(composition[0]) == 3
    assert isinstance(composition[0][0], VariableUnitValue)
    assert composition[0][1] == Model("id:E8zoYvN6m61A")


def test_association_download(client):
    """Test that associations are downloaded correctly."""
    composition = client.download(Object("id:XnlV5jKZwmp3"), "ResolvedOptions")
    assert isinstance(composition, dict)
    assert len(composition) == 295
    assert isinstance(composition["AbsorbanceSamplingRate"], VariableUnitValue)
    assert composition["AbsorbanceSamplingRate"].value == 20
    assert composition["Instrument"] == Object("id:wqW9BP4ARZVw")


def test_download_cloud_file(client):
    """Test that cloud file download correctly.

    This is the PhotoFile of Object("id:Z1lqpMzvkGMV").
    """
    cloud_file_path = client.download_cloud_file(Object("id:KBL5Dvw60ve7"))
    assert os.path.exists(cloud_file_path)


def test_download_cloud_file_with_byte_size(client):
    """Test that cloud file download correctly.

    This is the PhotoFile of Object("id:Z1lqpMzvkGMV").
    """
    cloud_file_path = client.download_cloud_file(Object("id:KBL5Dvw60ve7"), byte_size=10_000_000)
    assert os.path.exists(cloud_file_path)


def test_download_model(client):
    assert client.download(Object("id:qdkmxzGkAK0a"), "Container[Model]") == Model(
        id="id:L8kPEjkmLbvW", type="Model.Container.Plate"
    )


def test_resolve_type_mutates_objects(client):
    sample = Object("id:qdkmxzGkAK0a")
    _ = client.resolve_type(sample)
    assert sample.type == "Object.Sample"


def test_resolve_type_for_multiple_objects(client):
    assert [
        obj.type
        for obj in [
            client.resolve_type(kind)
            for kind in [
                Object("id:Z1lqpMzvkGMV"),
                Object("id:o1k9jAGmo6Jm"),
                Model("id:L8kPEjkmLbvW"),
            ]
        ]
    ] == [
        "Object.User.Emerald.Developer",
        "Object.User.Emerald.Developer",
        "Model.Container.Plate",
    ]


def test_resolve_type_overwrites_existing_type(client):
    obj = Object("id:Z1lqpMzvkGMV", type="Some.Crazy.Type")
    assert obj.type == "Some.Crazy.Type"
    _ = client.resolve_type(obj)
    assert obj.type == "Object.User.Emerald.Developer"


def test_resolve_type_listable_overload(client):
    objects = client.resolve_type(
        [
            Object("id:Z1lqpMzvkGMV"),
            Object("id:o1k9jAGmo6Jm"),
            Model("id:L8kPEjkmLbvW"),
        ]
    )
    [a, b, c] = objects
    assert (a.type, b.type, c.type) == (
        "Object.User.Emerald.Developer",
        "Object.User.Emerald.Developer",
        "Model.Container.Plate",
    )

    source = [Object("id:Z1lqpMzvkGMV"), Object("id:o1k9jAGmo6Jm"), Model("id:L8kPEjkmLbvW")]
    _ = client.resolve_type(iter(source))
    with pytest.raises(StopIteration):
        next(_)

    assert list(map(attrgetter("type"), source)) == [
        "Object.User.Emerald.Developer",
        "Object.User.Emerald.Developer",
        "Model.Container.Plate",
    ]


def test_resolve_type_on_non_existing_object(client):
    with pytest.raises(ConstellationObjectDoesNotExistException):
        _ = client.resolve_type(
            [
                Object("id:Z1lqpMzvkGMV"),
                Object("id:o1k9jAGmo6Jm"),
                Object("id:the_intruder"),
                Model("id:L8kPEjkmLbvW"),
            ]
        )


def test_simple_download_packet(client):
    packet = client.download(Object("id:Z1lqpMzvkGMV"), {"Name", "Email"})
    assert packet["Name"] == "bsmith"
    assert packet["Email"] == "bsmith@emeraldcloudlab.com"


def test_download_packet_for_multiple_objects(client):
    assert client.download(
        [
            Object("id:Z1lqpMzvkGMV"),
            Object("id:n0k9mG8070Mk"),
        ],
        {
            "Name",
            "Email",
        },
    ) == [
        {"Name": "bsmith", "Email": "bsmith@emeraldcloudlab.com"},
        {"Name": "service+manifold", "Email": "service+manifold@emeraldcloudlab.com"},
    ]


def test_packet_download_with_traversal(client):
    assert client.download(Object("id:Z1lqpMzvkGMV"), {"Name", "FinancingTeams[Name]"}) == {
        "FinancingTeams[Name]": ["Engineering"],
        "Name": "bsmith",
    }


def test_packet_download_with_repeats(client):
    assert client.download(Object("id:4pO6dM57V6K7"), {"Name", "Repeated[Container]"}) == {
        "Name": None,
        "Repeated[Container]": [
            Object("id:xRO9n3BdWrxY", type="Object.Container.MicrofluidicChip"),
        ],
    }


def test_packet_download_with_part(client):
    """Test downloading parts of a field."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), {"ProtocolsAuthored[[1]]"}) == {
        "ProtocolsAuthored[[1]]": Object("id:wqW9BP7dkv8G")
    }


def test_packet_download_with_part_and_traversal(client):
    """Test downloading parts of a field then traversing a link."""
    assert client.download(Object("id:Z1lqpMzvkGMV"), {"ProtocolsAuthored[[1]][Author]"}) == {
        "ProtocolsAuthored[[1]][Author]": Object("id:Z1lqpMzvkGMV")
    }
