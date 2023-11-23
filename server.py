from flask import Flask, Response, request, redirect

app = Flask(__name__)

def get_headers_for_partial_content(start, end, content_length):
    return {
        'Content-Range': f'bytes {start}-{end}/{content_length}',
        'Content-Length': str(end - start + 1),
        'Accept-Ranges': 'bytes',
        'Content-type': 'video/mp4'
    }

@app.route('/video.mp4', methods=['GET', 'HEAD'])
def stream_video():
    if request.method == 'HEAD':
        headers = {
            'Content-Length': '1048681',
            'Accept-Ranges': 'bytes',
            'Content-type': 'video/mp4'
        }
        return Response(status=200, headers=headers)
    else:
        range_header = request.headers.get('Range')
        start, end = map(int, range_header.replace('bytes=', '').split('-'))

        if start == 1048576 and end == 1048680:
            headers = {
                'Content-Length': '105',
                'Location': 'http://internal-api:8989/flag',
            }
            return '', 302, headers

        if start == 0 and end == 4:
            return b"\x00\x00\x00\x18"

        headers = get_headers_for_partial_content(start, end, 1048681)
        data = "A" * (end - start + 1)

        return Response(data, status=206, headers=headers)

if __name__ == '__main__':
    app.run(debug=True, port=8000, host="0.0.0.0")
