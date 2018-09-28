# Development Information

Information about and for the development of Seeking Shelter.

## To do

- [ ] Use marker icons that are easily recognisable
- [ ] Write About page
- [ ] Reorg `src/plot_interactive_geomap.py` to improve build process (currently running some things twice...)
- [ ] Decide whether to use a backend (e.g. places near me...instead of computation on client)
- [ ] Decide whether/which front-end framework to use
- [x] 'Near me' feature
- [x] Add `tel:` hyperlink to telephone numbers in popups
- [x] Make map display mobile friendly
- [x] Zoom to user's location
- [x] Provide separate basic and advanced maps
- [x] Add menu

## Setup

```
virtualenv src/env
source src/env/bin/activate
```

Then in the activated environment:

```
pip install -r requirements.txt
```

## Build

```
python src/build.py
```
