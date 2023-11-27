import tkinter as tk
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageDraw, ImageChops, ImageFilter
import os

class App:
    def __init__(self, window, window_title='FilTTer-aPP', window_width='1000', window_height='800'):
        self.window = window
        self.window.title(window_title)
        self.is_image_uploaded = False
        self.file_path = None
        self.current_webcam_frame = None
        self.is_Webcan = False
        self.webcam_images_path = 'images_webcam'
        self.stickers_path = "stickers"

        top_bottom_height = 15
        middle_height = 800 * 0.6

        frame1 = tk.Frame(self.window, height=top_bottom_height)
        frame2 = tk.Frame(self.window, height=middle_height)
        frame3 = tk.Frame(self.window, height=top_bottom_height)
        frame1.pack(fill=tk.X)
        frame2.pack(expand=True, fill=tk.BOTH)
        frame3.pack(fill=tk.X)

        def upload_image():
            self.file_path = filedialog.askopenfilename()
            if self.file_path:
                image = Image.open(self.file_path)
                img_width, img_height = image.size
                aspect_ratio = img_width / img_height

                new_width = 500
                new_height = int(new_width / aspect_ratio)

                image = image.resize((new_width, new_height), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(image)

                if not self.is_image_uploaded:
                    self.frame_img = tk.Frame(frame2)
                    self.frame_img.pack(expand=True, fill=tk.BOTH)
                    self.label_img = tk.Label(self.frame_img, image=img)
                    self.label_img.image = img
                    self.label_img.pack(pady=(10, 0))
                    self.is_image_uploaded = True
                else:
                    self.label_img.config(image=img)
                    self.label_img.image = img

            self.is_Webcan = False


        def open_webcam():
            cap = cv2.VideoCapture(0)  # Access default webcam (change the parameter for other webcams)

            if cap.isOpened():
                cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)  # Disable auto exposure
                cap.set(cv2.CAP_PROP_EXPOSURE, 0.5)  # Manually adjust exposure (vary between 0 and 1)

                ret, frame = cap.read()

                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert frame colors from BGR to RGB
                    img = Image.fromarray(frame)
                    img_width, img_height = img.size
                    aspect_ratio = img_width / img_height

                    new_width = 500
                    new_height = int(new_width / aspect_ratio)

                    img = img.resize((new_width, new_height), Image.ANTIALIAS)
                    img = ImageTk.PhotoImage(image=img)

                    if not self.is_image_uploaded:
                        self.frame_img = tk.Frame(frame2)
                        self.frame_img.pack(expand=True, fill=tk.BOTH)
                        self.label_img = tk.Label(self.frame_img, image=img)
                        self.label_img.image = img
                        self.label_img.pack(pady=(10, 0))
                        self.is_image_uploaded = True
                    else:
                        self.label_img.config(image=img)
                        self.label_img.image = img

                    # Save the webcam image to a specific directory
                    if not os.path.exists(self.webcam_images_path):
                        os.makedirs(self.webcam_images_path)
                    cv2.imwrite(f"{self.webcam_images_path}/webcam_image.jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

                    # Store the current webcam frame after resizing
                    self.current_webcam_frame = img
                    self.file_path = self.webcam_images_path + "/webcam_image.jpg"

            cap.release()

        def download_image():
            if self.is_image_uploaded:
                if not os.path.exists('images_download'):
                    os.makedirs('images_download')
        
                # Split the file path to get the image name
                image_name = os.path.basename(self.file_path)
        
                # Get the modified image from label_img and save it to the download directory
                img = self.label_img.image
                img_data = img._PhotoImage__photo.subsample(1)  # Retrieve modified image data
                img_data.write(f"images_download/{image_name}", format="png")  # Save as PNG format (or any desired format)
                print(f"Image '{image_name}' downloaded successfully.")
            else:
                print("No image uploaded.")

        # Row 2
        # Create a container frame to hold the buttons in the center
        button_frame = tk.Frame(frame2)
        button_frame.pack(expand=True)  # Expand to fill the available space
        # Create a button to trigger the image upload function
        upload_button = tk.Button(button_frame, text="Upload Image", command=upload_image, width=15, height=3, relief=tk.RAISED, borderwidth=3)
        upload_button.pack(side=tk.LEFT, padx=5, pady=5)

        webcam_button = tk.Button(button_frame, text="Webcam", command=open_webcam, width=15, height=3, relief=tk.RAISED, borderwidth=3)
        webcam_button.pack(side=tk.LEFT, padx=5, pady=5)

        download_button = tk.Button(button_frame, text="Download Image", command=download_image, width=15, height=3, relief=tk.RAISED, borderwidth=3)
        download_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Row 3
        
        filters_frame = tk.Frame(frame3)
        filters_frame.pack(expand=True, fill=tk.Y)  # Expandir horizontalmente para preencher o espaço disponível

        filters = ["Grayscale", "Sepia Tone", "Vintage", "HDR", "Commic Book",
           "Binarization", "Watercolor", "Gaussian Blur", "Emboss", "Smudge"]
        
        def apply_filter(filter_name):
            if filter_name == "Grayscale":  # Check if the selected filter is Filter 1 (Grayscale)
                if self.is_image_uploaded:
                        # Convert the image to grayscale
                        image = ImageOps.grayscale(Image.open(self.file_path))
                        img = ImageTk.PhotoImage(image)

                        # Update the label with the grayscale image
                        self.label_img.config(image=img)
                        self.label_img.image = img
                else:
                    print("Image not uploaded")
            elif filter_name == "Sepia Tone":
                if self.is_image_uploaded:
                    image = Image.open(self.file_path)
                    sepia = _apply_sepia_tone(image)
                    img = ImageTk.PhotoImage(sepia)
                    self.label_img.config(image=img)
                    self.label_img.image = img

            elif filter_name == "Vintage":
                if self.is_image_uploaded:
                    image = Image.open(self.file_path)
                    vintage = _apply_vintage(image)
                    img = ImageTk.PhotoImage(vintage)
                    self.label_img.config(image=img)
                    self.label_img.image = img

            elif filter_name == "HDR":
                if self.is_image_uploaded:
                    image = Image.open(self.file_path)
                    hdr = _apply_hdr(image)
                    img = ImageTk.PhotoImage(hdr)
                    self.label_img.config(image=img)
                    self.label_img.image = img
            
            elif filter_name == "Commic Book":
                if self.is_image_uploaded:
                    image = Image.open(self.file_path)
                    comic = _apply_comic_book_effect(image)
                    img = ImageTk.PhotoImage(comic)
                    self.label_img.config(image=img)
                    self.label_img.image = img

            elif filter_name == "Binarization":
                if self.is_image_uploaded:
                    image = Image.open(self.file_path)
                    binary = _apply_binarization(image)
                    img = ImageTk.PhotoImage(binary)
                    self.label_img.config(image=img)
                    self.label_img.image = img
            
            elif filter_name == "Watercolor":
                if self.is_image_uploaded:
                    image = Image.open(self.file_path)
                    water = _apply_watercolor_effect(image)
                    img = ImageTk.PhotoImage(water)
                    self.label_img.config(image=img)
                    self.label_img.image = img

            elif filter_name == "Gaussian Blur":
                if self.is_image_uploaded:
                    image = Image.open(self.file_path)
                    blur = _apply_gaussian_blur(image)
                    img = ImageTk.PhotoImage(blur)
                    self.label_img.config(image=img)
                    self.label_img.image = img

            elif filter_name == "Emboss":
                if self.is_image_uploaded:
                    image = Image.open(self.file_path)
                    emboss = _apply_emboss_effect(image)
                    img = ImageTk.PhotoImage(emboss)
                    self.label_img.config(image=img)
                    self.label_img.image = img
                
            else:
                if self.is_image_uploaded:
                    image = Image.open(self.file_path)
                    smudge = _apply_smudge_effect(image)
                    img = ImageTk.PhotoImage(smudge)
                    self.label_img.config(image=img)
                    self.label_img.image = img

        def _apply_sepia_tone(image):
            # Implementação do filtro Sepia Tone
            sepia_data = []
            sepia = ImageEnhance.Color(image.convert("L")).enhance(1.5).convert("RGB")
            for pixel in sepia.getdata():
                r, g, b = pixel
                tr = int(r * 0.393 + g * 0.769 + b * 0.189)
                tg = int(r * 0.349 + g * 0.686 + b * 0.168)
                tb = int(r * 0.272 + g * 0.534 + b * 0.131)
                sepia_data.append((tr, tg, tb))
            sepia.putdata(sepia_data)
            return sepia
        
        def _apply_vintage(image):
            vignette = Image.new('L', image.size, 255)
            width, height = image.size
            mask = Image.new('L', (width, height), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((width * 0.1, height * 0.1, width * 0.9, height * 0.9), fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(radius=30))  # Gaussian blur effect
            vignette.paste(mask, (0, 0))
            return ImageChops.multiply(image, vignette.convert('RGB'))
        
        def _apply_hdr(image):
            # Applies the HDR (High Dynamic Range) filter
            enhancer = ImageEnhance.Contrast(image)
            enhanced_img = enhancer.enhance(1.5)  # Increase contrast to bring out details
            enhancer = ImageEnhance.Brightness(enhanced_img)
            hdr_img = enhancer.enhance(1.2)  # Slightly increase brightness
            return hdr_img

        def _apply_comic_book_effect(image):
            # Applies the Comic Book Effect filter
            edges = image.filter(ImageFilter.FIND_EDGES)
            return edges
        
        def _apply_binarization(image):
            # Applies the Binarization filter
            threshold_value = 128  # Change this value as needed
            return image.convert("L").point(lambda x: 0 if x < threshold_value else 255, '1')
        
        def _apply_watercolor_effect(image):
            # Simulates a Watercolor Effect
            # Apply Gaussian blur to soften edges
            blurred_img = image.filter(ImageFilter.GaussianBlur(radius=10))
    
            # Enhance color to make them more vivid
            enhanced_img = ImageEnhance.Color(blurred_img).enhance(1.5)
    
            # Apply a texture or paper-like overlay
            paper_texture = Image.new('RGBA', image.size, (230, 240, 250, 180))
            paper_texture = paper_texture.resize(image.size)  # Resize texture to match image size
            watercolor_img = Image.blend(enhanced_img.convert('RGBA'), paper_texture, 0.2)  # Adjust the blending factor for texture
    
            return watercolor_img
        
        def _apply_gaussian_blur(image):
            # Applies the Gaussian Blur filter
            blurred_img = image.filter(ImageFilter.GaussianBlur(radius=5))  # Adjust the radius as needed
            return blurred_img
        
        def _apply_emboss_effect(image):
            # Applies the Emboss Effect
            embossed_img = image.filter(ImageFilter.EMBOSS)
            return embossed_img
        
        def _apply_smudge_effect(image):
            # Aplica o efeito de Esfumaçado (Smudge)
            # Aplica um desfoque gaussiano para suavizar a imagem
            blurred_img = image.filter(ImageFilter.GaussianBlur(radius=5))
    
            # Suaviza a imagem para simular o efeito de esfumaçado
            smudged_img = blurred_img.filter(ImageFilter.SMOOTH)
    
            return smudged_img
        
        for i, filter_name in enumerate(filters):
            filter_button = tk.Button(filters_frame, text=filter_name, command=lambda name=filter_name: apply_filter(name))
            filter_button.grid(row=0, column=i, padx=3, pady=2)
                
        self.window.geometry(window_width + "x" + window_height)
        self.window.mainloop()

App(tk.Tk())