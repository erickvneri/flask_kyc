# MIT License
#
# Copyright (c) 2022 erickvneri
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
from database import connection


def create_identity_media(
    name: str,
    content: bytes,
    length: int,
    type: str,
    content_extract: bytes,
    extract_length: int) -> tuple:
    """
    Attemts to store media content
    into the public.identity_media
    table.

    ::param name    str
    ::param content bytes
    ::param length  int
    """
    sql_query = """
    INSERT INTO identity_media (
        name,
        content,
        length,
        type,
        content_extract,
        extract_length,
        created_at,
        updated_at
    ) VALUES (
        %(name)s,
        %(content)s,
        %(length)s,
        %(type)s,
        %(content_extract)s,
        %(extract_length)s,
        NOW(), NOW()
    ) RETURNING
        uuid,
        created_at,
        name,
        length,
        extract_length;
    """
    params = dict(
        name=name,
        content=content,
        length=length,
        type=type,
        content_extract=content_extract,
        extract_length=extract_length)
    connection.pool.execute(sql_query, params)
    return connection.pool.fetchone()


def get_identity_media(uuid: str) -> tuple:
    """
    Attempts to read from the
    public.identity_media table
    based on the media uuid.

    ::param uuid str
    """
    sql_query = """
    SELECT
        name,
        content,
        length,
        created_at,
        content_extract,
        extract_length,
        updated_at
    FROM identity_media
    WHERE uuid = %(uuid)s
    """
    params = dict(uuid=uuid)
    connection.pool.execute(sql_query, params)
    return connection.pool.fetchone()


def delete_identity_media(uuid: str) -> tuple:
    """
    Attempts to phisically delete
    a row from the public.identity_media
    table according to its UUID.

    ::param uuid str
    """
    sql_query = """
    DELETE FROM identity_media
    WHERE uuid = %(uuid)s
    RETURNING TRUE;
    """
    params = dict(uuid=uuid)
    print(params)
    connection.pool.execute(sql_query, params)
    return connection.pool.fetchall()
