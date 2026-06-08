# WebAR Magic Card

A WebAR "magic card": point a phone browser at a printed marker and a video plays on it. Marker-based AR using [AR.js](https://github.com/AR-js-org/AR.js) + [A-Frame](https://aframe.io/) — runs entirely in the browser, no app install required.

The AR content is the video at `assets/clip.mp4`, which plays flat on the card when the marker is detected.

## Print the marker

Print `marker/jabra-marker.png` — now a full **AR card**: a call-to-action line ("Point your camera here to discover the extra dimensions you get with the Jabra Sound Plus App") printed above the bordered tracking marker. The tracking image is now a large, bold **"J+"** — kept deliberately simple so it tracks reliably (the old multi-line text didn't track). Print the **whole card** (caption + marker square) on white paper or card, sized so the marker square is roughly **5–8 cm**. Keep the marker square's solid **black border fully intact** with a white margin around it — do not crop it; the border is what the tracker locks onto. The caption is above the square and does not affect tracking. That printed sheet is "the card."

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

## The video on the card

The card plays the clip at `assets/clip.mp4` on a flat plane via the `<a-video>` element inside `<a-marker>` in `index.html`.

On iOS the video must stay `muted` and `playsinline`, and may need a screen tap to start (mobile autoplay restriction); `index.html` also kicks playback on `markerFound`.

## Use your own design on the card (custom marker)

This project uses a custom pattern marker (`marker/jabra.patt`, printed as `marker/jabra-marker.png`). To put your own artwork on the card instead:

1. Open the AR.js Marker Training generator: <https://ar-js-org.github.io/AR.js/three.js/examples/marker-training/examples/generator.html>
2. Upload your image to generate a `.patt` file and save it under `marker/` (e.g. `marker/custom.patt`).
3. In `index.html`, point the marker tag at your pattern:

   ```html
   <a-marker type="pattern" url="marker/custom.patt">
   ```

Note that custom markers still need a solid black square border to track well. (The old `marker/hiro.png` is left in the repo but is no longer the active marker.)

## Future upgrade note

To track **arbitrary artwork or photos** (not a square fiducial marker), switch from AR.js to the [MindAR](https://github.com/hiukim/mind-ar-js) image-tracking library, which does natural-feature image tracking.
