from pysll.models import Model


def test_model_equality():
    assert Model("id:123") == Model("id:123")
    assert Model("id:123") == Model("id:123", type="Model.User")
    assert Model("id:123", type="Model.User") == Model("id:123")
    assert Model("id:123", type="Model.User") == Model("id:123", type="Model.User")

    assert Model("id:123") != Model("id:456")
    assert Model("id:123", type="Model.Container") != Model("id:123", type="Model.User")
    assert Model("id:123", type="Model.Container") != Model("id:456", type="Model.Container")
    assert Model("id:123", type="Model.Container") != Model("id:456")
    assert Model("id:123") != Model("id:456", type="Model.User")


def test_model_str():
    assert Model("id:123").sll_style_type() == "Model[id:123]"
    assert Model("id:123", type="Model").sll_style_type() == "Model[id:123]"
    assert Model("id:123", type="Container").sll_style_type() == "Model[Container, id:123]"
    assert Model("id:123", type="Model.Container").sll_style_type() == "Model[Container, id:123]"
    assert Model("id:123", type="Model.User.Emerald").sll_style_type() == "Model[User, Emerald, id:123]"
