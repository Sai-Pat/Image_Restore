from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from features.grayscale.process import convert_to_grayscale
from features.face_tools.process import blur_faces
from features.face_detect.process import detect_faces
from features.maze_solver.process import solve_maze
from features.seam_carving.process import carve_seams
from features.stitching.process import stitch_images
from features.eye_tracking.stream import eye_tracking_stream
from features.eye_tracking.process import process_eye_tracking
from utils.file_handling import save_uploaded_file

FEATURES_INFO = {
    'grayscale': {'title': 'Grayscale Magic', 'icon': '🎨', 'description': 'Turn colorful memories into timeless monochrome.', 'action': 'Upload an image to convert to grayscale.', 'multi': False},
    'face_blur': {'title': 'Privacy Mode', 'icon': '🎭', 'description': 'Softly blur faces to keep things mysterious.', 'action': 'Upload an image to blur faces.', 'multi': False},
    'face_detect': {'title': 'Face Detection', 'icon': '🎯', 'description': 'Identify and highlight faces in your images.', 'action': 'Upload an image to detect faces.', 'multi': False},
    'stitch': {'title': 'Panorama Dream', 'icon': '🌌', 'description': 'Stitch multiple photos into a seamless landscape.', 'action': 'Upload 2 or more images to stitch them together.', 'multi': True},
    'maze': {'title': 'Maze Solver', 'icon': '🧭', 'description': 'Find the way out with a glowing magic path.', 'action': 'Upload a maze image to solve it.', 'multi': False},
    'seam': {'title': 'Content Aware Resize', 'icon': '✂️', 'description': 'Shrink images without losing the important parts.', 'action': 'Upload an image to reduce its width intelligently.', 'multi': False},
    'eye_track': {'title': 'Eye Tracker', 'icon': '👁️', 'description': 'Real-time magic eye tracking using your webcam or upload.', 'action': 'Upload an image/video or use your webcam to track eyes.', 'multi': False},
}

def home(request):
    features = [{'id': k, 'url': k, **v} for k, v in FEATURES_INFO.items()]
    return render(request, 'core/home.html', {'features': features})

def feature_view(request, feature_id):
    if feature_id not in FEATURES_INFO:
        return render(request, 'core/404.html')
        
    info = FEATURES_INFO[feature_id]
    context = {'feature': info, 'feature_id': feature_id}
    
    if request.method == 'POST':
        try:
            if info['multi']:
                files = request.FILES.getlist('image')
                if not files or len(files) < 2:
                    context['error'] = 'Please upload at least 2 images.'
                    return render(request, 'core/feature.html', context)
                    
                saved_paths = []
                for f in files:
                    path, _ = save_uploaded_file(f)
                    saved_paths.append(path)
                    
                if feature_id == 'stitch':
                    out_url = stitch_images(saved_paths)
                    context['result_url'] = out_url
            else:
                if 'image' not in request.FILES:
                    context['error'] = 'Please upload a file.'
                    return render(request, 'core/feature.html', context)
                    
                file = request.FILES['image']
                path, original_url = save_uploaded_file(file)
                context['original_url'] = original_url
                
                if feature_id == 'grayscale':
                    context['result_url'] = convert_to_grayscale(path)
                elif feature_id == 'face_blur':
                    context['result_url'] = blur_faces(path)
                elif feature_id == 'face_detect':
                    context['result_url'] = detect_faces(path)
                elif feature_id == 'maze':
                    context['result_url'] = solve_maze(path)
                elif feature_id == 'seam':
                    context['result_url'] = carve_seams(path)
                elif feature_id == 'eye_track':
                    out_url, is_video = process_eye_tracking(path)
                    context['result_url'] = out_url
                    context['is_video'] = is_video
                    
        except Exception as e:
            context['error'] = str(e)
            
    return render(request, 'core/feature.html', context)
