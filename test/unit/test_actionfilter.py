from actionfilter import ProbabilisticActionFilter, FilterGroup

from collections import Counter
import pytest
from unittest.mock import MagicMock


class TestProbabilisticActionFilter:
    def test_probability_distribution(self):
        actionfilter = ProbabilisticActionFilter(probability_success=0.8)

        outputs = Counter(actionfilter() for _ in range(1000000))
        prob_true = outputs[True] / sum(outputs.values())
        assert 0.8 == pytest.approx(prob_true, 0.01)


class TestFilterGroup:
    @pytest.mark.parametrize(
        "name, filters_return_values, output",
        [
            ("single_true", [True], True),
            ("single_false", [False], False),
            ("all_true", [True] * 3, True),
            ("last_false", [True, True, False], False),
            ("first_false", [False, True, True], False),
        ],
    )
    def test_filters(self, name, filters_return_values, output):
        mock_filters = [self._mock_filter(rv) for rv in filters_return_values]
        f = FilterGroup(filters=mock_filters)

        assert output is f()

    def test_shortcircuit(self):
        false_filter = self._mock_filter(False)
        true_filter = self._mock_filter(True)

        FilterGroup(filters=[false_filter, true_filter])()

        assert false_filter.call_count == 1
        assert true_filter.call_count == 0

    def _mock_filter(self, *return_values):
        mocked_filter = MagicMock()
        mocked_filter.side_effect = return_values
        return mocked_filter
