# osm-blame

_Who touched this element?_

osm-blame is a minimalist tool inspired by git blame, whicch only objective is to show informations about last modifications of an OpenStreetMap element, tag by tag. By default it shows also tags that once existed and were deleted.

## Basic usage

The script takes as argument the reference of the element under the form `<type>/<id>`.

The output is a table showing a list of the tags and info about last time it was altered.

```
$ ./osm-blame.py node/1987567153
    key                   value                                      user                version
--  --------------------  -----------------------------------------  ----------------  ---------
-   addr:city                                                        Rom1                     11
-   addr:country                                                     Rom1                     11
+   addr:housenumber      50                                         Kalaallit Nunaat          1
-   addr:postcode                                                    Rom1                     11
-   addr:street                                                      Rom1                     11
+   amenity               restaurant                                 Kalaallit Nunaat          1
+   cuisine               french                                     Kalaallit Nunaat          1
+   name                  Brasserie Excelsior                        Kalaallit Nunaat          1
+   opening_hours         Mo-Su 00:00-00:30,08:00-24:00              Xapitoun                  3
+   payment:credit_cards  yes                                        Kalaallit Nunaat          1
-   phone                                                            Rom1                     11
+   source                local_knowledge                            Kalaallit Nunaat          1
-   website                                                          Rom1                     11
+   wikipedia             fr:Brasserie Excelsior                     py_berrard                4
-   fax                                                              Rom1                     11
+   wikidata              Q2923998                                   nyuriks                   8
+   loc_name              L’Excel’                                   gendy54                   9
+   contact:fax           +33 3 83351848                             Rom1                     11
+   contact:phone         +33 3 83352457                             Rom1                     11
+   contact:website       https://www.brasserie-excelsior-nancy.fr/  Rom1                     11
```

About the symbols before each line: `+` means that the tag is still applied, `-` means that it was deleted and the following info is about the time it has been deleted.

## Options

* `-a LIST`, `--attribs LIST`: `LIST` is a comma-separated list of attributes to show (not including keys and values). Default is `user,version`. Possible attributes: `user`, `version`, `uid`, `changeset`, `timestamp`. Other attributes are possibles but vary from the element type. More informations about attributes on OpenStreetMap API documentation.
* `-c LIST`, `--changeset-tags LIST`: `LIST` is a comma-separated list of changeset tags to show. Default is none, as it is slower due to more API calls. Common changeset tags: `created_by`, `comment`, `source`, `imagery_used`. Other changeset tags are possible but more rare, see the [OSM changeset documentation](https://wiki.openstreetmap.org/wiki/Changeset#Tags_on_changesets)
* `-d`, `--hide-deleted`: Do not show deleted tags.

## Contribute

As you can notice, this tool is no more than a dirty script for now. I am no developper and any help is of course always welcome, especially for cleaning the code and making it more readable. Don't hesitate to take a look at the issue tracker.
