from src.testing.scene import show_result_3d
from src.testing.factories import create_cart, create_payload
from src.api.schema import Payload
from src.api.app import App
from src.testing.utils import log


def simulate(algo: str = "FFD", cart_size: int = 10):
    algo = algo.upper()
    if algo not in ["FFD", "GGA"]:
        raise ValueError("'algo' must be one of 'FFD', 'GGA'")
    log(f"Running {algo} simulation with {cart_size} item(s)...")
    product_data = create_cart(cart_size)
    payload = create_payload(cart_items=product_data, algo=algo)
    instance = App(Payload.model_validate(payload))
    instance.execute()
    show_result_3d(instance.created_bundles(), instance.unallocated())
