import torch.nn as nn

class Autoencoder(nn.Module):
    # usa questo senza flatten appena puoi
    # def __init__(self):
    #     super(Autoencoder, self).__init__()
    #     self.encoder = nn.Sequential(
    #         nn.Conv2d(channels, 32, kernel_size=8, stride=4),
    #         nn.ReLU(),
    #         nn.Conv2d(32, 64, kernel_size=4, stride=2),
    #         nn.ReLU(),
    #         nn.Conv2d(64, 64, kernel_size=3, stride=1),
    #         nn.ReLU()
    #     )
    #     self.decoder = nn.Sequential(
    #         nn.ConvTranspose2d(64, 64, kernel_size=3, stride=1),
    #         nn.ReLU(),
    #         nn.ConvTranspose2d(64, 32, kernel_size=4, stride=2),
    #         nn.ReLU(),
    #         nn.ConvTranspose2d(32, 3, kernel_size=8, stride=4),
    #         nn.Sigmoid()  # Sigmoid to ensure pixel values are between 0 and 1
    #     )
    def __init__(self, channels=1):
        super(Autoencoder, self).__init__()
        self.encoder = nn.Sequential(
                nn.Conv2d(channels, 32, kernel_size=8, stride=4),
                nn.ReLU(),
                nn.Conv2d(32, 64, kernel_size=4, stride=2),
                nn.ReLU(),
                nn.Conv2d(64, 64, kernel_size=3, stride=1),
                nn.ReLU()
            )
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(64, 64, kernel_size=3, stride=1),
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, kernel_size=4, stride=2),
            nn.ReLU(),
            nn.ConvTranspose2d(32, channels, kernel_size=8, stride=4),
            nn.Sigmoid()  # Sigmoid to ensure pixel values are between 0 and 1
        )

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x