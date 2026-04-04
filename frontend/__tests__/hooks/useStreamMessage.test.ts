import { renderHook, act, waitFor } from '@testing-library/react'
import { useStreamMessage } from '@/hooks/useStreamMessage'

// Mock fetch and TextEncoder/TextDecoder
global.fetch = jest.fn()

// Mock TextEncoder and TextDecoder for Node.js environment
const mockTextEncoder = class {
  encode(input: string) {
    const view = new Uint8Array(input.length)
    for (let i = 0; i < input.length; i++) {
      view[i] = input.charCodeAt(i)
    }
    return view
  }
}

const mockTextDecoder = class {
  decode(input?: Uint8Array) {
    if (!input) return ''
    return String.fromCharCode(...input)
  }
}

// Use any to suppress type errors for test mocks
// eslint-disable-next-line @typescript-eslint/no-explicit-any
;(global as any).TextEncoder = mockTextEncoder
// eslint-disable-next-line @typescript-eslint/no-explicit-any
;(global as any).TextDecoder = mockTextDecoder

describe('useStreamMessage', () => {
  beforeEach(() => {
    jest.clearAllMocks()
  })

  test('initializes with empty streamContent and isStreaming false', () => {
    const { result } = renderHook(() => useStreamMessage('conv-1'))
    
    expect(result.current.streamContent).toBe('')
    expect(result.current.isStreaming).toBe(false)
  })

  test('sets isStreaming to true when sending starts', async () => {
    const mockReadableStream = {
      getReader: jest.fn().mockReturnValue({
        read: jest.fn().mockResolvedValue({ done: true })
      })
    }
    
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      body: mockReadableStream
    })

    const { result } = renderHook(() => useStreamMessage('conv-1'))
    
    await act(async () => {
      await result.current.sendStreaming('test message')
    })

    // After streaming completes, isStreaming should be false
    await waitFor(() => {
      expect(result.current.isStreaming).toBe(false)
    })
  })

  test('accumulates stream content from server', async () => {
    const encoder = new global.TextEncoder()
    const chunks = [
      { done: false, value: encoder.encode('Hello ') },
      { done: false, value: encoder.encode('World') },
      { done: true }
    ]
    let chunkIndex = 0

    const mockReader = {
      read: jest.fn().mockImplementation(() => {
        const result = chunks[chunkIndex]
        chunkIndex++
        return Promise.resolve(result)
      })
    }

    const mockReadableStream = {
      getReader: jest.fn().mockReturnValue(mockReader)
    }
    
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      body: mockReadableStream
    })

    const { result } = renderHook(() => useStreamMessage('conv-1'))
    
    await act(async () => {
      await result.current.sendStreaming('test message')
    })

    await waitFor(() => {
      expect(result.current.streamContent).toBe('Hello World')
    })
  })

  test('sends POST request with correct headers and body', async () => {
    const mockReadableStream = {
      getReader: jest.fn().mockReturnValue({
        read: jest.fn().mockResolvedValue({ done: true })
      })
    }
    
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      body: mockReadableStream
    })

    const { result } = renderHook(() => useStreamMessage('conv-123'))
    
    await act(async () => {
      await result.current.sendStreaming('test message')
    })

    expect(global.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/conversations/conv-123/messages/stream'),
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({
          'Content-Type': 'application/json'
        }),
        body: JSON.stringify({ content: 'test message' })
      })
    )
  })

  test('sets isStreaming to false after streaming completes', async () => {
    const mockReadableStream = {
      getReader: jest.fn().mockReturnValue({
        read: jest.fn().mockResolvedValue({ done: true })
      })
    }
    
    ;(global.fetch as jest.Mock).mockResolvedValueOnce({
      body: mockReadableStream
    })

    const { result } = renderHook(() => useStreamMessage('conv-1'))
    
    expect(result.current.isStreaming).toBe(false)
    
    await act(async () => {
      await result.current.sendStreaming('test message')
    })

    await waitFor(() => {
      expect(result.current.isStreaming).toBe(false)
    })
  })
})
