==========
Chronotope
==========

This package contains application code for the project
**Time has come today** by **Leuphana Universität Lüneburg**.


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


Contributors
============

- Robert Niederreiter

- Holger Schwetter

- Leuphana Universität Lüneburg
