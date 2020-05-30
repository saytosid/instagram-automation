from actionfilter import ProbabilisticActionFilter, FilterGroup

from collections import Counter
import pytest


class TestProbabilisticActionFilter:
    def test_probability_distribution(self):
        actionfilter = ProbabilisticActionFilter(probability_success=0.8)

        outputs = Counter(actionfilter() for _ in range(1000000))
        prob_true = outputs[True] / sum(outputs.values())
        assert 0.8 == pytest.approx(prob_true, 0.01)
