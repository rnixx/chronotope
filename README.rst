==========
Chronotope
==========

This package contains application code for the project
**Time has come today** by **Leuphana Universität Lüneburg**.

The chronotope is a concept used in literary theory and philosophy of language
to describe how configurations of time and space are represented in language
and discourse. (http://en.wikipedia.org/wiki/Chronotope)


Installation
============

For installation resources and instructions please refer to::

    https://github.com/rnixx/chronotope-buildout

Credits
=======

- Indexing Inspirations at https://github.com/wwitzel3/sawhoosh


Contributors
============

- Robert Niederreiter (Author)
- Holger Schwetter
- Leuphana Universität Lüneburg
- TU Dresden


History
=======

0.7
---

- Use ``bdajax.register`` function as introduced in ``bdajax`` 1.9.
  [rnix]

- Fix URL quote/unquote with ``cone.app`` 1.0a6. Quoting is done in
  ``make_url`` and ``make_query`` directly, so unquoting only needs to be done
  when reading from request parameters.
  [rnix]

- Customize main menu and add link to tutorial. Add tutorial tile which gets
  displayed as overlay and tutorial text to settings.
  [rnix]

- Cast float columns in ``search_locations`` in order to make location search
  work on lat/lon.
  [rnix]

- Change datatype of facility ``exists_from`` and ``exists_to`` fields from
  datetime to string. Exact date is not always known so a user may enter just
  a year.
  [rnix]

- Publish facility related locations if facility gets published but related
  locations are not published yet.
  [rnix]

- Add tooltip for map markers containing facility name and street/city.
  [rnix]

- Add note that email address not gets published.
  [rnix]

0.6
---

- Add Intro overlay.
  [rnix]

- Update ``bdajax`` to ``1.8``.
  [rnix]

0.5
---

- Implement browser history support.
  [rnix]

- Update ``bdajax`` to ``1.7``.
  [rnix]

- Update ``cone.app`` to ``1.0a4``.
  [rnix]

- Use ``cone.sql`` as base for model.
  [rnix]

0.4.2
-----

- Remove terms of use link from footer.
  [rnix]

0.4.1
-----

- Display links to terms of use and privacy policy in german translation of
  accept terms widget.
  [rnix]

- About dropdown reordering.
  [rnix]

0.4
---

- Add checkbox to accept terms of use for anonymous submitters.
  [rnix]

- Also check for empty submitter and published state when displaying edit note
  for locations.
  [rnix]

- Add privacy policy to about section.
  [rnix]

- Project has moved to TU Dresden. Adopt logo and link in footer.
  [rnix]

0.3
---

- Close SQL session properly.
  [rnix]

0.2
---

- Add terms of use.
  [rnix]

0.1
---

- make it work
  [rnix]
