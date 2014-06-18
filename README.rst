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


Model
=====

* Location
    * Lat (Float)
    * Lon (Float)
    * Street (String)
    * Zip (String)
    * City (String)
    * Country (String)

* Facilitiy
    * Title (String)
    * Description (String)
    * Exists from (Date)
    * Exists to (Date)
    * Category (List of Strings)
    * Location (List of Reference UID's)

* Occasion
    * Title
    * Description
    * Duration From (Date)
    * Duration To (Date)
    * Facility (List of Reference UID's)

* Attachment
    * Payload (File, Image or Text)
    * Location (List of Reference UID's)
    * Facility (List of Reference UID's)
    * Occasion (List of Reference UID's)


Contributors
============

- Robert Niederreiter
- Holger Schwetter
- Leuphana Universität Lüneburg
