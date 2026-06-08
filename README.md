# WebAR Magic Card

A WebAR "magic card": point a phone browser at a printed Hiro marker and a rotating 3D cube appears floating above it. Marker-based AR using [AR.js](https://github.com/AR-js-org/AR.js) + [A-Frame](https://aframe.io/) — runs entirely in the browser, no app install required.

## Print the marker

Print `marker/hiro.png` at roughly **5–8 cm square**, on white paper or card. Keep the solid **black border fully intact** — do not crop it; the border is what the tracker locks onto. That printed sheet is "the card."

## Test locally (desktop webcam)

```bash
cd ~/projects/webar-card
python3 -m http.server 8080
```

Then open <http://localhost:8080> in a browser, allow camera access, and hold the marker (printed, or just shown on another screen) in front of the webcam. `localhost` is exempt from the HTTPS-camera rule, so this works without any certificate setup.

## Test on a phone (needs HTTPS)

Browsers only grant camera access over **HTTPS**, so a plain `http://<your-ip>:8080` will not work on a phone. Two options:

- **Tunnel it:** run `ngrok http 8080` and open the generated `https://…` URL on the phone.
- **Host it:** push this folder to a free static host (GitHub Pages / Netlify / Cloudflare Pages) and open that HTTPS link on the phone.

## Tips

- Use good, even lighting and hold the marker steady.
- If tracking is jittery, print the marker **larger** and keep the **black border clean** (no smudges, no glare, no fold across it).

## Optional: play a video instead of the cube

Drop a short clip at `assets/clip.mp4`, then **uncomment** both the `<a-video>` block inside `<a-marker>` and the `<a-assets>` block in `index.html`.

On iOS the video must stay `muted` and `playsinline`, and may need a screen tap to start (mobile autoplay restriction).

## Use your own design on the card (custom marker)

To put your own artwork on the card instead of the default Hiro pattern:

1. Open the AR.js Marker Training generator: <https://ar-js-org.github.io/AR.js/three.js/examples/marker-training/examples/generator.html>
2. Upload your image to generate a `.patt` file and save it under `marker/` (e.g. `marker/custom.patt`).
3. In `index.html`, change the marker tag from `preset="hiro"` to:

   ```html
   <a-marker type="pattern" url="marker/custom.patt">
   ```

Note that custom markers still need a solid black square border to track well.

## Future upgrade note

To track **arbitrary artwork or photos** (not a square fiducial marker), switch from AR.js to the [MindAR](https://github.com/hiukim/mind-ar-js) image-tracking library, which does natural-feature image tracking.
