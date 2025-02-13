from ...element_iterator import ElementIterator
from ..namespace import Namespace
from ..page import Page


def test_page():
    XML = """
    <page>
        <title>AccessibleComputing</title>
        <ns>0</ns>
        <id>10</id>
        <redirect title="Computer accessibility" />
        <revision>
          <id>233192</id>
          <timestamp>2001-01-21T02:12:21Z</timestamp>
          <contributor>
            <username>RoseParks</username>
            <id>99</id>
          </contributor>
          <comment>*</comment>
          <model>wikitext</model>
          <format>text/x-wiki</format>
          <text xml:space="preserve">Text of rev 233192</text>
          <sha1>8kul9tlwjm9oxgvqzbwuegt9b2830vw</sha1>
        </revision>
        <revision>
          <id>862220</id>
          <parentid>233192</parentid>
          <timestamp>2002-02-25T15:43:11Z</timestamp>
          <contributor>
            <username>Conversion script</username>
            <id>0</id>
          </contributor>
          <minor />
          <comment>Automated conversion</comment>
          <model>wikitext</model>
          <format>text/x-wiki</format>
          <text xml:space="preserve">Text of rev 862220</text>
          <sha1>i8pwco22fwt12yp12x29wc065ded2bh</sha1>
        </revision>
    </page>
    """
    page = Page.from_element(ElementIterator.from_string(XML))
    assert page.id == 10
    assert page.title == "AccessibleComputing"
    assert page.namespace == 0
    assert page.redirect == "Computer accessibility"
    assert page.restrictions == []  # Should be known to be empty

    revision = next(page)
    assert revision.id == 233192
    assert revision.page == page

    revision = next(page)
    assert revision.id == 862220

def test_page_with_colon_in_title():
    XML = """
    <page>
        <title>Accessible: Computing</title>
        <ns>0</ns>
        <id>10</id>
        <redirect title="Computer accessibility" />
        <revision>
          <id>233192</id>
          <timestamp>2001-01-21T02:12:21Z</timestamp>
          <contributor>
            <username>RoseParks</username>
            <id>99</id>
          </contributor>
          <comment>*</comment>
          <model>wikitext</model>
          <format>text/x-wiki</format>
          <text xml:space="preserve">Text of rev 233192</text>
          <sha1>8kul9tlwjm9oxgvqzbwuegt9b2830vw</sha1>
        </revision>
    </page>
    """
    # When namespace_map is empty, it works:
    page = Page.from_element(ElementIterator.from_string(XML))
    assert page.id == 10
    assert page.title == "Accessible: Computing"
    assert page.namespace == 0
    assert page.redirect == "Computer accessibility"
    assert page.restrictions == []  # Should be known to be empty

    revision = next(page)
    assert revision.id == 233192
    assert revision.page == page

    # And when it's present, it still works the same:
    page = Page.from_element(ElementIterator.from_string(XML), namespace_map={})
    assert page.id == 10
    assert page.title == "Accessible: Computing"
    assert page.namespace == 0
    assert page.redirect == "Computer accessibility"
    assert page.restrictions == []  # Should be known to be empty

    revision = next(page)
    assert revision.id == 233192
    assert revision.page == page

def test_old_page():
    XML = """
    <page>
        <title>Talk:AccessibleComputing</title>
        <id>10</id>
        <redirect title="Computer accessibility" />
        <revision>
          <id>233192</id>
          <timestamp>2001-01-21T02:12:21Z</timestamp>
          <contributor>
            <username>RoseParks</username>
            <id>99</id>
          </contributor>
          <comment>*</comment>
          <model>wikitext</model>
          <format>text/x-wiki</format>
          <text xml:space="preserve">Text of rev 233192</text>
          <sha1>8kul9tlwjm9oxgvqzbwuegt9b2830vw</sha1>
        </revision>
    </page>
    """
    page = Page.from_element(ElementIterator.from_string(XML),
                             {"Talk": Namespace(1, "Talk")})
    assert page.namespace == 1


def test_page_with_discussion():
    XML = """
    <page>
        <title>Talk:AccessibleComputing</title>
        <ns>1</ns>
        <id>10</id>
        <redirect title="Computer accessibility" />
        <DiscussionThreading>
          <ThreadSubject>Foo</ThreadSubject>
          <ThreadParent>1</ThreadParent>
          <ThreadAncestor>2</ThreadAncestor>
          <ThreadPage>Bar</ThreadPage>
          <ThreadPage>3</ThreadPage>
          <ThreadAuthor>Baz</ThreadAuthor>
          <ThreadEditStatus>Herp</ThreadEditStatus>
          <ThreadType>Derp</ThreadType>
        </DiscussionThreading>
        <revision>
          <id>862220</id>
          <parentid>233192</parentid>
          <timestamp>2002-02-25T15:43:11Z</timestamp>
          <contributor>
            <username>Conversion script</username>
            <id>0</id>
          </contributor>
          <minor />
          <comment>Automated conversion</comment>
          <model>wikitext</model>
          <format>text/x-wiki</format>
          <text xml:space="preserve">Text of rev 862220</text>
          <sha1>i8pwco22fwt12yp12x29wc065ded2bh</sha1>
        </revision>
    </page>
    """
    page = Page.from_element(ElementIterator.from_string(XML),
                             {"Talk": Namespace(1, "Talk")})
    assert page.namespace == 1

    revision = next(page)
    assert revision.id == 862220
