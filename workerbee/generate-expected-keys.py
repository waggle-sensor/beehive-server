#!/usr/bin/env python3
from datetime import datetime, timedelta

expected_nodes = [
    '001e0610ba46',
    '001e0610ba5c',
    '001e0610ba3b',
    '001e0610ba67',
    '001e0610ba89',
    '001e0610ef75',
    '001e0610f02f',
    '001e06108081',
    '001e0610ba8f',
    '001e0610ba16',
    '001e06107e5d',
    '001e0610ba93',
    '001e0610b9eb',
    '001e0610ba8b',
    '001e0610ba3f',
    '001e0610bc03',
    '001e0610ba13',
    '001e0610ba18',
    '001e0610ba01',
    '001e0610bc10',
    '001e0610bbf9',
    '001e0610ba51',
    '001e0610bbff',
    '001e0610bc09',
    '001e0610b9e7',
    '001e0610ba15',
    '001e0610ba37',
    '001e0610bbe5',
    '001e0610ee33',
    '001e0610b9e5',
    '001e0610f8f4',
    '001e0610ee41',
    '001e0610e80f',
    '001e0610eef4',
    '001e0610eb9d',
    '001e0610f72c',
    '001e0610ef29',
    '001e0610f668',
    '001e0610f730',
    '001e0610bc07',
    '001e0610ef26',
    '001e0610ea5a',
    '001e0610ee61',
    '001e0610ba81',
    '001e0610ba57',
    '001e061135c8',
    '001e0610f068',
    '001e0610f8fd',
    '001e0610f029',
    '001e0610ef03',
    '001e0610eef6',
    '001e0610ee82',
    '001e0610f8f7',
    '001e0610ef66',
    '001e0610ee8d',
    '001e0610ef27',
    '001e0610fb4c',
    '001e0610ee6f',
    '001e0610ef68',
    '001e0610e809',
    '001e0610ee36',
    '001e061135cb',
    '001e0610e532',
    '001e0610e8cb',
    '001e0610f063',
    '001e0610ee5d',
    '001e0610ef73',
    '001e0610f8f6',
    '001e0610f725',
    '001e0610e540',
    '001e0611320d',
    '001e0610ef1d',
    '001e0610f6dd',
    '001e0610fc2d',
    '001e061130fe',
    '001e0610e547',
    '001e0610e34e',
    '001e06113ad8',
    '001e06115388',
    '001e06113a07',
    '001e0610e545',
    '001e06113d6d',
    '001e0611441e',
    '001e06115363',
    '001e06113d83',
    '001e06112e77',
    '001e0610e7fc',
    '001e0610f6db',
    '001e06115365',
    '001e0611325e',
    '001e06113cff',
    '001e0611537d',
    '001e06113107',
    '001e06114fd4',
    '001e0610890f',
    '001e06113ad6',
    '001e06109f62',
    '001e06113ace',
    '001e061146bc',
    '001e06113a24',
    '001e061144cd',
    '001e061146cb',
    '001e061144d6',
    '001e0610e539',
    '001e0610f703',
    '001e0610b9e9',
    '001e0611462f',
    '001e06115369',
    '001e06113d78',
    '001e061130f7',
    '001e0610bc12',
    '001e0610e835',
    '001e0610e538',
    '001e0610eef2',
    '001e061130f4',
    '001e0611536a',
    '001e0610ee43',
    '001e0610f05c',
    '001e0610f732',
    '001e06113100',
    '001e0610e537',
    '001e0610f513',
    '001e06109416',
    '001e061146d6',
    '001e0610ee5f',
    '001e06113d22',
    '001e06113ae8',
    '001e06113d20',
    '001e06114503',
    '001e06113dbc',
    '001e061144c0',
    '001e06114fcf',
    '001e061146d4',
    '001e06109401',
    '001e06115382',
    '001e06113cf1',
    '001e06113acb',
    '001e06114640',
    '001e06113f54',
    '001e06114500',
    '001e06113d32',
    '001e061146ba',
    '001e06113a48',
    '001e06113ba6',
    '001e06115379',
    '001e06114fd6',
    '001e061146b8',
    '001e0611463b',
    '001e0611536c',
    '001e0611538f',
    '001e06114fd9',
    '001e061182e8',
    '001e06118501',
    '001e06118404',
    '001e06117b41',
    '001e06117b45',
    '001e061182a1',
    '001e061183eb',
    '001e061182c1',
    '001e06118509',
    '001e06118182',
    '001e061181b6',
    '001e0611844c',
    '001e061184e7',
    '001e061183ec',
    '001e0611844a',
    '001e06118578',
    '001e061182a9',
    '001e06118295',
    '001e061183fc',
    '001e061182a3',
    '001e061182e7',
    '001e061181e8',
    '001e06118433',
    '001e061183bf',
    '001e06117f33',
    '001e0611804d',
    '001e06118128',
    '001e061182a2',
    '001e061144be',
    '001e06107c9e',
    '001e0610c5fa',
    '001e0610c069',
    '001e0610c0ea',
    '001e0610c040',
    '001e0610c219',
    '001e0610c2e5',
    '001e0610c042',
    '001e0610c2eb',
    '001e0610c2e9',
    '001e0610c2e3',
    '001e0610c42e',
    '001e0610c2df',
    '001e0610c429',
    '001e0610c06b',
    '001e0610c2db',
    '001e0610c6f4',
    '001e0610c2d7',
    '001e0610c2e1',
    '001e0610c2ed',
    '001e0610c2dd',
    '001e0610c776',
    '001e0610c0ef',
    '001e0610c762',
    '001e0610c2a9',
    '001e0610c046',
    '001e0610c044',
    '001e0610c2e7',
    '001e0610c03e',
    '001e0610c5ed',
    '001e0610c216',
    '001e0610889b',
    '001e0610ba8d',
    '001e061134fa',
    '001e061134f3',
    '001e0610ba64',
    '001e06107d97',
    '020000000000',
    '0242809503d3',
    '001e061088bf',
    '001e06107e4c',
    '001e061080a7',
    '001e06107fa0',
    '001e06200367',
    '001e061089e5',
    '001e0620051e',
    '001e06200325',
    '001e061088a6',
    '001e06107cc5',
    '001e061088c8',
    '001e06108a8a',
    '001e0610ba4e',
    '001e06107d70',
    '001e0610941b',
    '001e06118447',
    '001e0611849b',
    '001e0611850f',
    '001e061182a8',
    '001e06118502',
    '001e0611856d',
    '001e061184a3',
    '001e06117b44',
    '001e061183f3',
    '001e061182b5',
    '001e061182b1',
    '001e06118577',
    '001e061183f5',
    '001e061182a7',
    '001e061182b4',
    '001e06118435',
    '001e06118057',
    '001e0611845a',
    '001e06118571',
    '001e06118364',
    '001e06118195',
    '001e061184e3',
    '001e061182ae',
    '001e061182b0',
    '001e06117fd0',
    '001e06118448',
    '001e06117a4b',
    '001e061183e4',
    '001e06117fd1',
    '001e061182b2',
    '001e06117b4b',
    '001e06117f31',
    '001e061182aa',
    '001e061183ba',
    '001e06117f2e',
    '001e061182b3',
    '001e06117fcf',
    '001e06117fb4',
    '001e06117a36',
    '001e0611805d',
    '001e061183b9',
    '001e061184e5',
    '001e0611805a',
    '001e061181bc',
    '001e061184e1',
    '001e061183fe',
    '001e06118629',
    '001e06117b42',
    '001e06117b40',
    '001e06117d8e',
    '001e061182ac',
    '001e061183bb',
    '001e06118383',
    '001e061184e2',
    '001e06117b46',
    '001e06117f2c',
    '001e06118211',
    '001e06117fcc',
    '001e06118367',
    '001e0611863a',
    '001e06118129',
    '001e06118164',
    '001e06118178',
    '001e06117f46',
    '001e06117f9f',
    '001e061182af',
    '001e06118459',
    '001e061182a5',
    '001e06117f32',
    '001e06117f37',
    '001e061184fc',
    '001e06117fd8',
    '001e061181b9',
    '001e0611768b',
    '001e06118366',
    '001e0611842f',
    '001e06118572',
    '001e06118197',
    '001e061182bb',
    '001e061184de',
    '001e06118162',
    '001e06118384',
    '001e06117f3b',
    '001e0611815f',
    '001e06118385',
    '001e06118198',
    '001e06117fcb',
    '001e061182be',
    '001e06117a37',
    '001e061183f8',
    '001e06117a53',
    '001e061182bf',
    '001e06117a33',
    '001e06118434',
    '001e061182bc',
    '001e06117f9e',
    '001e061181b5',
    '001e061184e0',
    '001e06118450',
    '001e061182b6',
    '001e061182b7',
    '001e06117f36',
    '001e061181ba',
    '001e061182c0',
    '001e06117a4f',
    '001e061183bd',
    '001e06117f30',
    '001e0611849c',
    '001e06118381',
    '001e06117fb1',
    '001e061181bb',
    '001e0611845b',
    '001e0611849e',
    '001e06113131',
    '001e0610ee9b',
    '001e061089d5',
    '001e0610f715',
    '001e06113d30',
    '001e06108a80',
    '001e06109dee',
    '001e06114646',
    '001e06113d39',
    '001e06113d6f',
    '001e06114631',
    '001e06113ad0',
    '001e06113aa2',
    '001e061146d3',
    '001e06114645',
    '001e06200193',
    '001e061135c6',
    '001e06112a81',
    '001e0611249c',
    '000000000001',
    '000000000002',
    '001e061183c0',
    'f00000000001',
    'f00000000002',
    '001e061182a4',
    '001e061184e6',
    '001e061182ab',
    '001e0611854e',
    '001e06118400',
    '001e06118296',
    '001e06118407',
    '001e06118405',
    '001e061183fd',
    '001e06117a59',
    '001e061089d3',
    '001e06118436',
    '001e061182a6',
    '001e06200364',
    '001e0611805c',
    '001e06118168',
    '001e061182c4',
    '001e06118167',
    '001e061184fb',
    '001e06117a38',
    '001e061131d6',
    '001e0610ea32',
    '001e06200335',
    '001e06107d7f',
]

today = datetime.today()
yesterday = datetime.today() - timedelta(days=1)

for node in expected_nodes:
    print(node, yesterday.date())
    print(node, today.date())