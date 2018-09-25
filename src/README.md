# Development Information

Information about and for the development of Seeking Shelter.

## To do

- [ ] Use marker icons that are easily recognisable
- [ ] Add `tel:` hyperlink to telephone numbers in popups
- [ ] Write About page
- [ ] 'Shelters near me' feature?
- [ ] Reorg `src/plot_interactive_geomap.py` to improve build process (currently running some things twice...)
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
