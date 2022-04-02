from run import app
import app.charts as chart

def test_should_return_string_get_amount_chart() :
    result = chart.get_amount_chart()
    assert isinstance(result, str)
