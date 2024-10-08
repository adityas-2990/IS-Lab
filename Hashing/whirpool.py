from Crypto.Hash import Whirlpool

message = b"Test message"
hash_obj = Whirlpool.new()
hash_obj.update(message)
digest = hash_obj.hexdigest()

print("Whirlpool Hash:", digest)
