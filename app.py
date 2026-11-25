"""Streamlit respiration project GUI. M2: audio filtering and envelope plots."""

from hashlib import sha256

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from scipy.signal import spectrogram

from dsp import AUDIO_CONFIG, analyze_audio, prepare_audio, read_wav


def draw_waveform(axis, samples, sample_rate, title, color):
    """Keep min/max amplitudes in display bins; never downsample analysis audio."""
    bin_size = max(1, int(np.ceil(len(samples) / 3000)))
    starts = np.arange(0, len(samples), bin_size)
    lower = np.minimum.reduceat(samples, starts)
    upper = np.maximum.reduceat(samples, starts)
    times = (starts + np.minimum(bin_size, len(samples) - starts) / 2) / sample_rate
    axis.fill_between(times, lower, upper, color=color, alpha=0.75)
    axis.set(title=title, ylabel="Amplitude (input units)", xlim=(0, len(samples) / sample_rate))
    axis.grid(alpha=0.2)


def show_signal_plots(recording, prepared, analysis):
    """Render acoustic and rhythm plots with separate frequency interpretations."""
    config = analysis["config"]
    audio_band = f"{config['audio_band_hz'][0]:g}–{config['audio_band_hz'][1]:g} Hz"
    envelope_band = f"{config['envelope_band_hz'][0]:g}–{config['envelope_band_hz'][1]:g} Hz"
    start, end = analysis["analysis_start_s"], analysis["analysis_end_s"]
    duration = prepared["duration_s"]
    st.caption(
        f"Cycle-analysis interval: {start:.2f}–{end:.2f} s ({end - start:.2f} s). "
        "Gray margins are excluded from later cycle analysis; the full clip was filtered first."
    )
    with st.expander("Filter and envelope settings"):
        st.write(
            f"Audio band: {config['audio_band_hz'][0]:g}–{config['audio_band_hz'][1]:g} Hz. "
            f"Envelope band: {config['envelope_band_hz'][0]:g}–{config['envelope_band_hz'][1]:g} Hz."
        )
        st.write(
            f"RMS window: {config['rms_window_s'] * 1000:g} ms; "
            f"hop: {config['rms_hop_s'] * 1000:g} ms; "
            f"envelope sample rate: {analysis['envelope_sample_rate']:g} Hz."
        )
        st.write(
            f"Both bands use Butterworth IIR, design N={config['filter_design_order']}, "
            f"SOS, forward-backward filtering: order {2 * config['filter_design_order']} per pass, "
            f"effective response order {4 * config['filter_design_order']}."
        )
        st.write(
            "The audio band contains audible sound. The much slower envelope band follows "
            "changes in sound energy. The envelope cutoffs define a search range of "
            f"{60 * config['envelope_band_hz'][0]:g}–{60 * config['envelope_band_hz'][1]:g} BPM. "
            "These cutoffs are starting choices for pilot testing."
        )

    st.subheader("Original and filtered waveforms")
    figure, axes = plt.subplots(2, 1, figsize=(9, 4.8), sharex=True, layout="constrained")
    draw_waveform(axes[0], recording["original_audio"].mean(axis=1), recording["source_sample_rate"],
                  "Original waveform (mono channel average)", "#52667a")
    draw_waveform(axes[1], analysis["filtered_audio"], analysis["sample_rate"],
                  f"Audio after {audio_band} band-pass", "#0f766e")
    axes[1].set_xlabel("Time (s)")
    for axis in axes:
        axis.axvspan(0, start, color="gray", alpha=0.12)
        axis.axvspan(end, duration, color="gray", alpha=0.12)
    st.pyplot(figure)
    plt.close(figure)

    st.subheader("Audio spectrogram")
    frequencies, times, power = spectrogram(
        prepared["audio"], fs=prepared["sample_rate"], window="hann",
        nperseg=512, noverlap=256, detrend=False, scaling="density", mode="psd"
    )
    power_db = 10 * np.log10(np.maximum(power, 1e-20))
    figure, axis = plt.subplots(figsize=(9, 3.5), layout="constrained")
    image = axis.pcolormesh(times, frequencies, power_db, shading="auto", cmap="magma",
                            vmin=float(power_db.max()) - 80, vmax=float(power_db.max()), rasterized=True)
    axis.set(title="Input audio spectrum before band-pass (16 kHz mono)",
             xlabel="Time (s)", ylabel="Acoustic frequency (Hz)", xlim=(0, duration))
    figure.colorbar(image, ax=axis, label="PSD (dB re 1 unit²/Hz)")
    st.pyplot(figure)
    plt.close(figure)
    st.caption("The spectrogram uses DC-removed, resampled audio before the analysis band-pass.")

    st.subheader("RMS envelope and filtered rhythm")
    figure, axes = plt.subplots(2, 1, figsize=(9, 4.8), sharex=True, layout="constrained")
    axes[0].plot(analysis["envelope_time_s"], analysis["rms"], color="#52667a", linewidth=1.2)
    axes[0].set(title="Short-time RMS of filtered audio", ylabel="RMS (input units)")
    axes[1].plot(analysis["envelope_time_s"], analysis["rhythm"], color="#0f766e", linewidth=1.3)
    axes[1].axhline(0, color="gray", linewidth=0.5)
    axes[1].set(title=f"Filtered envelope ({envelope_band})", xlabel="Time (s)", ylabel="Amplitude (input units)")
    for axis in axes:
        axis.set_xlim(0, duration)
        axis.axvspan(0, start, color="gray", alpha=0.12)
        axis.axvspan(end, duration, color="gray", alpha=0.12)
        axis.grid(alpha=0.2)
    st.pyplot(figure)
    plt.close(figure)
    st.caption("The filtered envelope is signed. A visible bump is not yet a verified breathing cycle.")


def main():
    st.set_page_config(page_title="Respiration Rate Estimator", page_icon="🎙️", layout="centered")
    st.title("Respiration Rate Estimator")
    st.caption("An educational audio and digital signal processing project.")
    st.write("Record or upload a breathing sample to begin.")
    st.info("Explore the waveform, spectrogram, and envelope. Cycle detection and breathing-rate estimation come next.")

    with st.expander("Recording tips and supported files"):
        st.write(
            "Use a quiet room and keep your microphone position steady. "
            "Record 30 to 120 seconds of comfortable breathing; aim for about 60 seconds. "
            "Avoid talking or touching the microphone during the recording."
        )
        st.write("Supported: mono or stereo WAV, at least 8000 Hz, up to 50 MB.")
        st.caption("Educational demonstration only. Not a medical diagnostic tool.")

    input_method = st.radio("Audio source", ["Upload WAV", "Record audio"], horizontal=True)
    if input_method == "Upload WAV":
        uploaded = st.file_uploader("Choose a breathing recording", type=["wav"], key="uploaded_audio")
    else:
        st.caption("Allow microphone access if your browser asks, then stop recording when finished.")
        uploaded = st.audio_input("Record a breathing sample", key="recorded_audio")

    audio_bytes = uploaded.getvalue() if uploaded is not None else None
    token = (input_method, sha256(audio_bytes).hexdigest()) if audio_bytes else None
    if st.session_state.get("audio_token") != token:
        st.session_state["audio_token"] = token
        st.session_state.pop("prepared_audio", None)
        st.session_state.pop("analysis", None)

    if uploaded is None:
        st.button("Analyze audio", disabled=True)
        st.caption("Your recording will appear here with playback and file details.")
        return

    try:
        recording = read_wav(audio_bytes)
    except ValueError as error:
        st.session_state.pop("prepared_audio", None)
        st.session_state.pop("analysis", None)
        st.error(str(error))
        st.button("Analyze audio", disabled=True)
        return

    st.subheader("Your recording")
    st.caption(uploaded.name)
    st.audio(audio_bytes, format="audio/wav")
    duration_column, rate_column, channel_column = st.columns(3)
    duration_column.metric("Duration", f"{recording['duration_s']:.1f} s")
    rate_column.metric("Sample rate", f"{recording['source_sample_rate']:,} Hz")
    channel_column.metric("Channels", "Mono" if recording["channels"] == 1 else "Stereo")

    if st.button("Analyze audio", type="primary"):
        st.session_state.pop("prepared_audio", None)
        st.session_state.pop("analysis", None)
        try:
            with st.spinner("Filtering audio and extracting its envelope..."):
                prepared = prepare_audio(recording)
                analysis = analyze_audio(prepared)
                st.session_state["prepared_audio"] = prepared
                st.session_state["analysis"] = analysis
        except ValueError as error:
            st.error(str(error))

    prepared = st.session_state.get("prepared_audio")
    if prepared is not None:
        st.success("Audio filtered and envelope extracted successfully.")
        st.write(
            f"The audio is mono at {prepared['sample_rate']:,} Hz with the DC offset removed. "
            "The original recording is kept without peak normalization."
        )
        with st.expander("Preparation details"):
            st.write(f"Prepared samples: {len(prepared['audio']):,}")
            st.write(f"Prepared duration: {prepared['duration_s']:.2f} seconds")
            st.write(f"Removed DC offset: {prepared['dc_offset']:+.6f}")
            st.write("Resampled: " + ("Yes" if prepared["resampled"] else "Not needed"))
            st.caption(f"Processing sample rate: {AUDIO_CONFIG['sample_rate']:,} Hz")
        analysis = st.session_state.get("analysis")
        if analysis is not None:
            for warning in analysis["warnings"]:
                st.warning(warning)
            show_signal_plots(recording, prepared, analysis)

    st.caption("Educational demonstration only. Not a medical diagnostic tool.")


if __name__ == "__main__":
    main()
