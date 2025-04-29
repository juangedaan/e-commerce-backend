from unittest.mock import MagicMock
from app.services.product_service import list_products

def test_list_products():
    db = MagicMock()
    mock_products = [{"id": 1, "title": "Item"}]
    db.query.return_value.all.return_value = mock_products

    result = list_products(db)

    assert result == mock_products
    db.query.assert_called_once()

