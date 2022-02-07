#  coding=utf-8
#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from typing import List

import pytest

import rubrix as rb
from rubrix.client.dataset import MixedRecordTypesError, WrongRecordTypeError


@pytest.fixture
def records() -> List[rb.TextClassificationRecord]:
    return [rb.TextClassificationRecord(inputs=f"{i}") for i in range(3)]


def test_init(records):
    dataset = rb.Dataset()

    assert dataset._records == []
    assert dataset._record_type is None

    dataset = rb.Dataset(records)

    assert dataset._records is records
    assert dataset._record_type is type(records[0])

    with pytest.raises(
        MixedRecordTypesError,
        match="but you provided more than one: .*TextClassificationRecord.*Text2TextRecord.*",
    ):
        rb.Dataset(
            [
                rb.TextClassificationRecord(inputs="mock"),
                rb.Text2TextRecord(text="mock"),
            ]
        )


def test_iter_len_getitem(records):
    dataset = rb.Dataset(records)

    for record, expected in zip(dataset, records):
        assert record == expected

    assert len(dataset) == 3
    assert dataset[1] is records[1]


def test_setitem(records):
    dataset = rb.Dataset(records)

    record = rb.TextClassificationRecord(inputs="mock")
    dataset[0] = record

    assert dataset._records[0] is record

    with pytest.raises(
        WrongRecordTypeError,
        match="You are only allowed to set a record of type .*TextClassificationRecord.* but you provided .*Text2TextRecord.*",
    ):
        dataset[0] = rb.Text2TextRecord(text="mock")


def test_append(records):
    dataset = rb.Dataset()
    record = rb.TextClassificationRecord(inputs="mock")

    dataset.append(record)

    assert dataset._record_type == type(record)
    assert dataset._records[-1] is record

    with pytest.raises(
        WrongRecordTypeError,
        match="You are only allowed to append a record of type .*TextClassificationRecord.* but you provided .*Text2TextRecord.*",
    ):
        dataset.append(rb.Text2TextRecord(text="mock"))
