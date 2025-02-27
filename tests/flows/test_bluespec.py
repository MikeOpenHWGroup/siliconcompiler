import siliconcompiler

import os
import pytest

@pytest.mark.quick
@pytest.mark.eda
def test_bluespec(datadir):
    src = os.path.join(datadir, 'FibOne.bsv')
    chip = siliconcompiler.Chip()
    chip.add('source', src)
    chip.set('design', 'mkFibOne')
    chip.set('frontend', 'bluespec')
    chip.target('asicflow_freepdk45')

    chip.run()

    assert chip.find_result('gds', step='export') is not None
