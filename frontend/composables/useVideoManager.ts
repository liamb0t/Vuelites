interface VideoInstance {
  id: string
  videoRef: HTMLVideoElement
  audioRef?: HTMLAudioElement
  pause: () => void
}

const activeVideos = new Map<string, VideoInstance>()

export const useVideoManager = () => {
  const registerVideo = (id: string, videoRef: HTMLVideoElement, audioRef?: HTMLAudioElement, pauseCallback?: () => void) => {
    const pause = () => {
      videoRef.pause()
      audioRef?.pause()
      pauseCallback?.()
    }

    activeVideos.set(id, {
      id,
      videoRef,
      audioRef,
      pause
    })
  }

  const unregisterVideo = (id: string) => {
    activeVideos.delete(id)
  }

  const playVideo = (currentId: string) => {
    // Pause all other videos
    activeVideos.forEach((video, id) => {
      if (id !== currentId) {
        video.pause()
      }
    })
  }

  const pauseAllVideos = () => {
    activeVideos.forEach(video => {
      video.pause()
    })
  }

  return {
    registerVideo,
    unregisterVideo,
    playVideo,
    pauseAllVideos
  }
}